import requests, json, os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
key = os.environ.get('key')
url = 'http://192.168.1.105/api/'

df = pd.read_excel('Schüler.xlsx')
df['Meter'] = 0
for i in range(len(df.index)):
    if df.at[i,'Vorname'] == 1 or df.at[i,'Familienname'] == 1:
        print('finished')
        break
    name = df.at[i,'Vorname'] + ' ' + df.at[i,'Familienname'] 
    klasse = str(df.at[i,'Klasse'])
    code = str(df.at[i,'Code'])
    c = requests.get(url + 'meter/' + code, headers={'Authorization': key})
    c_text = json.loads(c.text)
    print(code)
    meter = c_text['meter']
    df.at[i, 'Meter'] = meter
    
df.to_excel('Schüler_export.xlsx', index=False)
    
    
