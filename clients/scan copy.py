import os, requests, json, colorama
from colorama import Fore
from playsound3 import playsound
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get('key')
url = os.environ.get('url')

r = requests.get(url + 'test', headers={'Authorization': key})
r_text = json.loads(r.text)
if r_text['status'] == 'ok':
    print(Fore.GREEN + 'Bereit!')
else:
    print(Fore.RED + 'Authentifizierung fehlgeschlagen')

try:
    while True:
        code = input(Fore.WHITE + 'Code: ')
        if code == 'stop':
            break
        t = requests.get(url + 'scanned/' + code, headers={'Authorization': key})
        if t.status_code == 200:
            t_text = json.loads(t.text)
            name = t_text['name']
            if t_text['status'] == 'ok':
                runde = t_text['kilometer']
                print(Fore.GREEN + 'Erfolgreich gescanned!')
                print('Name: ' + name + ' Runde: ' + str(runde))
                print()
                playsound("success.wav", block=False)
            elif t_text['status'] == 'zu schnell':
                print(Fore.YELLOW + name + ' war zu schnell!!! (Scan wird nicht gewertet)')
                print()
                playsound("zu-schnell.wav", block=False)
        else:
            print(Fore.RED + 'Server Error!')
            print()
            playsound("error.wav", block=False)
finally:
    print("Programm gestoppt.")
