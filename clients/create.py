import requests, json
from barcode import ITF
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get('key')
url = 'http://127.0.0.1:8000/api/'

name = 'Leonard Alexander Stegle, 9b'
c = requests.get(url + 'create/' + name, headers={'Authorization': key})
c_text = json.loads(c.text)
code = c_text["code"]
print(code)

barcode = ITF(code, writer=ImageWriter())
barcode.save(code)

pdf = canvas.Canvas(name + '.pdf')
pdf.setTitle('Sponsorenlauf' + name)
pdf.rotate(90)
pdf.setFontSize(30)
pdf.drawString(20, -100, 'Sponsorenlauf 2023')
pdf.setFontSize(15)
pdf.drawString(20, -150, name)
pdf.drawImage(code + '.png', -80, -450, width=400, height=250)
pdf.line(300, 0, 300, -2000)
pdf.save()
