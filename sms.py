import smtplib
import os
from email.message import EmailMessage

# Borrowed code from Reddit post:
# https://www.reddit.com/r/Python/comments/8gb88e/free_alternatives_to_twilio_for_sending_text/

carriers = {
    'att': '@txt.att.net',
    'tmobile': ' @tmomail.net',
    'verizon': '@vtext.com',
    'sprint': '@page.nextel.com'
}


def send(message: str):
    # Replace the number with your own, or consider using an argument\dict for multiple people.
    if 'GMAIL_USER' not in os.environ:
        print("ERROR: Make sure to set GMAIL_USER in environment")
        return False

    if 'GMAIL_PW' not in os.environ:
        print("ERROR: Make sure to set GMAIL_PW in environment")
        return False

    user = os.environ['GMAIL_USER']
    pw = os.environ['GMAIL_PW']

    print(user + " " + pw)
    to_number = '5302638988{}'.format(carriers['att'])
    auth = (user, pw)

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    msg = EmailMessage()
    msg['Subject'] = "Automated message from me"
    msg['From'] = user
    msg['To'] = to_number
    msg.set_content(message)

    # Send text message through SMS gateway of destination number
    server.sendmail(auth[0], to_number, msg.as_string())
    return True
