import os, requests, json, colorama
from colorama import Fore
#import winsound
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get('key')
url = 'http://192.168.1.105/api/'

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
 #               winsound.PlaySound("success.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
            elif t_text['status'] == 'zu schnell':
                print(Fore.YELLOW + name + ' war zu schnell!!! (Scan wird nicht gewertet)')
                print()
  #              winsound.PlaySound("zu-schnell.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
        else:
            print(Fore.RED + 'Server Error!')
            print()
 #           winsound.PlaySound("error.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
finally:
    print("Programm gestoppt.")

