import smtplib,ssl
import os
from email.message import EmailMessage
import imghdr

def send_mail(img_path):
    host = "smtp.gmail.com"
    port = 587
    username = "mail@gmail.com"
    password = os.getenv("PASSWORD")
    receiver = "mail@gmail.com"

    email_mess = EmailMessage()
    email_mess['Subject'] = "There is an Intruder"
    email_mess.set_content("OMG Call 911")

    with open(img_path, 'rb') as file:
        image = file.read()

    email_mess.add_attachment(image, maintype='image', subtype=imghdr.what(None, image))

    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(username, receiver,email_mess.as_string())
        server.quit()


if __name__ == "__main__":
    send_mail("images/1.png")