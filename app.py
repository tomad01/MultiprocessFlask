from flask import Flask,request,json,session
import time,pdb,re
import multiprocessing,logging


app = Flask(__name__)
app.secret_key = 'super secret key'
MAX_QUEUE_SIZE = 10 
MAX_NR_OF_PROCESSES = 4

def worker_function(task_queue,log_queue,stop_queue):
    while 1:
        args = task_queue.get()
        if args is None: break
        time.sleep(2)    
        log_queue.put(f'worker {multiprocessing.current_process().name} finished job {args}')
    stop_queue.put(f'stopping {multiprocessing.current_process().name} end')
     
@app.route('/tasks_status',methods=['GET'])
def get_tasks_status(): 
    jobs = _queue.qsize()     
    response = app.response_class(
        response=json.dumps(f'we have curently {jobs} jobs in progress, all jobs from this session: {session.get("jobs")}'),
        mimetype='application/json'
    )
    return response

@app.route('/run_task',methods=['GET'])
def run_new_task(): 
    if  _queue.qsize() < MAX_QUEUE_SIZE:
        _queue.put(request.args.to_dict()['job_name'])     
        if 'jobs' in session:
            session['jobs']+=1
        else:
            session['jobs']=1
        message = 'worker started'
    else: 
        message = 'two many items in the queue'

    response = app.response_class(
        response=json.dumps(message),
        mimetype='application/json'
    )
    return response

def listener(task_queue,max_nr_of_processes):
    logging.basicConfig(filename='logs.log',
                    filemode='w',
                    format='%(asctime)s, %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
    logger = logging.getLogger()                   

    processes = {}
    log_queue = multiprocessing.Queue() 
    stop_queue = multiprocessing.Queue() 
    multiprocessing.log_to_stderr()
    #logger = multiprocessing.get_logger()
    #logger.setLevel(logging.INFO)    
    
    logger.info('starting main process')
    last_nr_of_tasks = 0 
    while 1:        
        request = task_queue.qsize()
        
        if request==last_nr_of_tasks:            
            time.sleep(1)
        else:
            last_nr_of_tasks = request


        needed_threads = request if request<max_nr_of_processes else max_nr_of_processes
        existing_threads = len(processes)
        need_to_stop = existing_threads - needed_threads
        need_to_raise = needed_threads - existing_threads
        #logger.info(f'need to stop {need_to_stop} processes {need_to_raise} {existing_threads} {request}')  
        if need_to_stop>0: 
            for _ in range(need_to_stop):
                logger.info(f'need to stop {need_to_stop} processes')    
                task_queue.put(None)
                m = stop_queue.get()          
                proc_name = re.search('stopping\s(.+)\send', m).group(1)
                processes.pop(proc_name).join()
                logger.info(m)
            logger.info(f'current nr of processes {len(processes)}')
        if need_to_raise>0:  
            logger.info(f'need to start {need_to_raise} processes')    
            for _ in range(need_to_raise):
                proc = multiprocessing.Process(target=worker_function, args=(task_queue,log_queue,stop_queue))                
                proc.start()
                logger.info(f'starting worker {proc.name}\n')       
                processes[proc.name] = proc
            logger.info(f'current nr of processes {len(processes)}')
        while not log_queue.empty():                
            m = log_queue.get()                  
            logger.info(m)                    



if __name__ == '__main__':
    
    _queue = multiprocessing.Queue()    
    watcher = multiprocessing.Process(target=listener, args =(_queue,MAX_NR_OF_PROCESSES,)).start()
    app.run(debug=True)