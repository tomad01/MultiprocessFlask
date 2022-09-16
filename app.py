from flask import Flask,request,json
import time,pdb,re
import multiprocessing,logging


app = Flask(__name__)
MAX_QUEUE_SIZE = 10 
MAX_NR_OF_PROCESSES = 4

def worker_function(duration:int,queue):
    time.sleep(duration)    
    queue.put(f'worker {multiprocessing.current_process().name} finished in {duration} seconds')
     
@app.route('/tasks_status',methods=['GET'])
def get_tasks_status(): 
    jobs = _queue.qsize()     
    response = app.response_class(
        response=json.dumps(f'we have curently {jobs} jobs in progress'),
        mimetype='application/json'
    )
    return response

@app.route('/run_task',methods=['GET'])
def run_new_task(): 
    duration = request.args.get('worker_duration')  

    if  _queue.qsize() < MAX_QUEUE_SIZE:
        _queue.put(int(duration))         
        message = 'worker started'
    else: 
        message = 'two many items in the queue'

    response = app.response_class(
        response=json.dumps(message),
        mimetype='application/json'
    )
    return response

def listener(task_queue,max_nr_of_processes):
    fn = 'processes.log'
    processes = {}
    log_queue = multiprocessing.Queue() 
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)    
    with open(fn, 'w') as f:
        f.write('starting main process\n')
        f.flush()
        while 1:                      
            if not log_queue.empty():
                m = log_queue.get()          
                proc_name = re.search('worker\s(.+)\sfinished', m).group(1)
                processes.pop(proc_name).join()
                f.write(str(m) + '\n')
                f.flush()         
            else:
                try:
                    task = task_queue.get(timeout=5)  
    
                    proc = multiprocessing.Process(target=worker_function, args=(task,log_queue,))
                    
                    proc.start()
                    f.write(f'starting worker {proc.name}\n')
                    f.flush()
                    processes[proc.name]=proc
                except Exception as er:
                    pass
                    # ignore empty queue error
                    #f.write(f'Error {str(er)}\n')
                    #f.flush()
            
            # safety
            if len(processes)==max_nr_of_processes:
                f.write('cleaning all processes\n')
                f.flush()                
                for process in processes.values():
                    process.join()
                    try:
                        m = log_queue.get()
                        if m:
                            f.write(str(m) + '\n')
                            f.flush()
                    except Exception as er:
                        #f.write(f'Error {str(er)}\n')
                        #f.flush()                        
                        pass
                # make sure all processes are joined
                #multiprocessing.active_children()
                processes = {}

if __name__ == '__main__':
    
    _queue = multiprocessing.Queue()    
    watcher = multiprocessing.Process(target=listener, args =(_queue,MAX_NR_OF_PROCESSES,)).start()
    app.run(debug=True)