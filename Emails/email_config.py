import smtplib
from Emails.email_content import file_901_fee


def send_email(sender, recipient):
    smtpObjtest = smtplib.SMTP('smtp.gmail.com', 587)

    smtpObjtest.ehlo()
    smtpObjtest.starttls()

    get_password = input('Please input your password: ')

    smtpObjtest.login(sender, get_password)

    smtpObjtest.sendmail(sender, recipient, file_901_fee)

send_email(sender='nmbenzo@gmail.com', recipient='nbenzschawel@usfca.edu')