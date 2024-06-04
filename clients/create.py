import requests, json, os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
key = os.environ.get('key')
url = 'http://192.168.1.105/api/'

df = pd.read_excel('Schüler.xlsx')
for i in range(len(df.index)):
    if df.at[i,'Vorname'] == 1 or df.at[i,'Familienname'] == 1:
        print('finished')
        break
    name = df.at[i,'Vorname'] + ' ' + df.at[i,'Familienname'] 
    klasse = str(df.at[i,'Klasse'])
    code = str(df.at[i,'Code'])
    c = requests.get(url + 'create/' + name + '/' + klasse + '/' + code, headers={'Authorization': key})
    c_text = json.loads(c.text)
    if c_text["status"] == "klasse nicht gefunden":
        d = c = requests.get(url + 'createklasse/' + klasse, headers={'Authorization': key})
        d_text = json.loads(d.text)
        if d_text["status"] == "created":
            print('Klasse ' + d_text["name"] + ' erstellt')
            c = requests.get(url + 'create/' + name + '/' + klasse + '/' + code, headers={'Authorization': key})
            c_text = json.loads(c.text)
    if c_text["status"] == "created":
        print('> Schüler ' + c_text["name"] + ' erstellt')
    else:
        print('-!!!error!!!')
    
