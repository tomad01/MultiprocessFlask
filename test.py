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
for job in [1,2,4,3]:    
    rr = s.get(url = URL, params = {'worker_duration':job})
    print(rr.json())
    time.sleep(1)
URL = f'http://127.0.0.1:5000/tasks_status'
rr = s.get(url = URL)
print(rr.json())