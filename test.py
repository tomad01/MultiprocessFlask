import json
from app import app
from urllib.parse import urlencode
PARAMS = {'worker_duration':3}    

# app.app.config['TESTING'] = True
# client = app.app.test_client()
# url = 'run_task' + '?' + urlencode(PARAMS)
# response = client.get(url)
# print(json.loads(response.data.decode('utf-8')))



import requests
URL = f'http://127.0.0.1:5000/run_task'
rr = requests.get(url = URL, params = PARAMS)
print(rr.json())
URL = f'http://127.0.0.1:5000/tasks_status'
rr = requests.get(url = URL)
print(rr.json())