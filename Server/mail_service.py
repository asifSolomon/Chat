import os
import random
import smtplib
import ssl

port = 465  # For SSL

smtp_server = "smtp.gmail.com"
sender_email = os.environ['sender_email']
password = os.environ['password']


# email with code
def forgotPass_email(receiver_email):
    num = random.randint(0, 999999)

    message = f"""\
    Subject: reset password

    Hi,
    How are you?
    Here is your code:

    {num}

    """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return num

# welcome email
def join_email(receiver_email, user, Fname):
    message = f"""\
    Subject: Welcome!

    Hi {Fname},
    Welcome to chat2U
    
    Your user is: {user}
    """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
