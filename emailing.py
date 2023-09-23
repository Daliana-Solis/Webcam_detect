import smtplib
from email.message import  EmailMessage
import imghdr


sender = '#email'
passw = '#email password'

def send_email(image_path):
    email_msg = EmailMessage()
    email_msg["subject"] = "New object"

    #Email body
    email_msg.set_content("New object was detected")

    with open(image_path, "rb") as file:
        content = file.read()

    #attach image content to email
    email_msg.add_attachment(content, maintype = "image", subtype=imghdr.what(None, content))

    #Login gmail
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, passw)

    #Send email
    gmail.sendmail(sender, sender, email_msg.as_string())
    gmail.quit()


if __name__ == '__main__':
    send_email(image_path="images/50.png")