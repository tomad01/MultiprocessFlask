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
for _ in range(100):
    rr = s.get(url = URL, params = {'worker_duration':2})
    print(rr.json())
    time.sleep(.1)
    rr = s.get(url = URL2)
    print(rr.json())