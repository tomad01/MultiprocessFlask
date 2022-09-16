import json,time
from app import app
from urllib.parse import urlencode


# app.app.config['TESTING'] = True
# client = app.app.test_client()
# url = 'run_task' + '?' + urlencode(PARAMS)
# response = client.get(url)
# print(json.loads(response.data.decode('utf-8')))



import requests
s = requests.Session()
URL = f'http://127.0.0.1:5000/run_task'
URL2 = f'http://127.0.0.1:5000/tasks_status'

rr = s.get(url = URL, params = {'worker_duration':2,'job_name':'job1'})
print(rr.json())

time.sleep(4)
for i in range(1,11):
    rr = s.get(url = URL, params = {'worker_duration':2,'job_name':f'job{i+1}'})
    print(rr.json())
    time.sleep(.1)
    #rr = s.get(url = URL2)
    #print(rr.json())
time.sleep(4)
rr = s.get(url = URL, params = {'worker_duration':2,'job_name':f'job12'})
print(rr.json())
time.sleep(4)
rr = s.get(url = URL2)
print(rr.json())