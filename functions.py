import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email():
    sender_email = "speechrecapp36@gmail.com"
    receiver_email = "" #enter receiver email
    password = "dhrckuswjrsegaiu"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Speech recognition"
    message["From"] = sender_email
    message["To"] = receiver_email

    texte = """\
    Hi,
    Speech recognised:
    """
    html = """\
    <html>
      <body>
        <p>"""+text+"""<br>
            <br>
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(texte, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        print("Sent")