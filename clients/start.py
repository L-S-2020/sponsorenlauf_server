import os, requests, json
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get('key')
url = 'http://192.168.1.132/api/'


h = requests.get(url + 'start', headers={'Authorization': key})
h_text = json.loads(h.text)
print(h_text)
