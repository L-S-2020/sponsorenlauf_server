import os, requests, json, time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from playsound3 import playsound
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get('key')
url = os.environ.get('url')

console = Console()

def flash_white():
    console.clear()
    console.print(Panel(
        "",
        style="on white",
        border_style="white",
        expand=True,
        height=console.height - 2,
    ))
    time.sleep(0.2)

def show_result(title, body_text, style):
    content = Text(body_text, justify="center", style=f"bold white on {style}")
    console.clear()
    console.print(Panel(
        Align(content, align="center", vertical="middle"),
        title=title,
        style=f"on {style}",
        border_style=f"bold {style}",
        expand=True,
        height=console.height - 4,
    ))

r = requests.get(url + 'test', headers={'Authorization': key})
r_text = json.loads(r.text)
if r_text['status'] == 'ok':
    show_result("Bereit", "Scanner aktiv", "green")
else:
    show_result("✗ Fehler", "Authentifizierung fehlgeschlagen", "red")

try:
    while True:
        code = input('\nCode: ')
        if code == 'stop':
            break
        t = requests.get(url + 'scanned/' + code, headers={'Authorization': key})
        if t.status_code == 200:
            t_text = json.loads(t.text)
            name = t_text['name']
            if t_text['status'] == 'ok':
                runde = t_text['kilometer']
                flash_white()
                show_result("✓ Erfolgreich gescannt", f"{name}\nRunde {runde}", "green")
                playsound("success.wav", block=False)
            elif t_text['status'] == 'zu schnell':
                show_result("⚠ Zu schnell!", f"{name}\nwird nicht gewertet", "yellow")
                playsound("zu-schnell.wav", block=False)
        else:
            show_result("✗ Fehler", "Server-Fehler", "red")
            playsound("error.wav", block=False)
finally:
    print("Programm gestoppt.")
