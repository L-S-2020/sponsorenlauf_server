import requests, json
import pandas as pd
from colorama import Fore
from time import sleep

key = 'VEXKrIDx0i9oKiOFKXzTB57ny4MSqHBh'
url = 'http://192.168.1.105/api/'

df = pd.read_excel('Schüler.xlsx')
try:
    while True:
        for i in range(len(df.index)):
            sleep(0.5)
            code = str(df.at[i,'Code'])
            t = requests.get(url + 'scanned/' + code, headers={'Authorization': key})
            if t.status_code == 200:
                    t_text = json.loads(t.text)
                    name = t_text['name']
                    if t_text['status'] == 'ok':
                        runde = t_text['kilometer']
                        print(Fore.GREEN + 'Erfolgreich gescanned!')
                        print('Name: ' + name + ' Runde: ' + str(runde))
                        print()
                    elif t_text['status'] == 'zu schnell':
                        print(Fore.YELLOW + name + ' war zu schnell!!! (Scan wird nicht gewertet)')
                        print()
            else:
                print(Fore.RED + 'Server Error!')
                print()
finally:
    print("Programm gestoppt.")
    
