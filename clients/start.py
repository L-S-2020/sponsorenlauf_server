import os, requests, json

key = 'VEXKrIDx0i9oKiOFKXzTB57ny4MSqHBh'
url = 'http://192.168.1.105/api/'


h = requests.get(url + 'start', headers={'Authorization': key})
h_text = json.loads(h.text)
print(h_text)
