import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Template

from ..settings import MAIL_PASSWORD


current_path = os.path.dirname(os.path.realpath(__file__))

from_address = "hack.masters@mail.ru"

with open(os.path.join(current_path, "template.html"), encoding="utf8") as file:
    html = file.read()


def send_mail(link, to_address="dmitriy1d01@gmail.com"):

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = "Авторизация в мульти-чатах"

    template = Template(html)
    body = template.render(link=link)

    msg.attach(MIMEText(body, "html"))

    server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
    # server.starttls()
    server.login(from_address, MAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()
