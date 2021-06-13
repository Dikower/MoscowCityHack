import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_address = "hack.masters@mail.ru"
to_address = "dmitriy1d01@gmail.com"

with open('../secrets.json', 'r', encoding='utf8') as file:
    password = json.load(file)['password']

msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address
msg['Subject'] = "Авторизация в мульти-чатах"

# body = "Это пробное сообщение"
with open('template.html', encoding='utf8') as file:
    body = file.read()

msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
# server.starttls()
server.login(from_address, password)
text = msg.as_string()
server.sendmail(from_address, to_address, text)
server.quit()
