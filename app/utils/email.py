import os
from flask import current_app
from flask_mail import Message
from app import mail



def sendPasswordResetToken(recipient, url):
    msg = Message("Hello",
                  sender=current_app.config['MAIL_SENDGRID_SENDER'],
                  recipients=[recipient])
    msg.body = f"Please visit this {url} to reset your password. The address is valid for 10 minutes."
    msg.html = f"<b>Please visit this {url} to reset your password. The address is valid for 10 minutes.</b>"

    try:
        mail.send(msg)
    except Exception as e:
        print(e.body)
