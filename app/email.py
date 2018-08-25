from flask_mail import Message
from app import app, mail
from flask import render_template

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	mail.send(msg)

def email_password_reset(user):
    token = user.get_reset_password_token()
    send_email('Reset your UniGO password', sender=app.config['ADMINS'][0], recipients=[user.email], \
    	text_body=render_template('email/reset-password.txt', user=user, token=token),\
    	html_body=render_template('email/reset-password.html', user=user, token=token))