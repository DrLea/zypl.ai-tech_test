import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def send_email(recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, recipient_email, text)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {str(e)}")


def send_email_notification(follower_email, author_name, music_name):
    try:
        if not follower_email or not author_name or not music_name:
            raise ValueError("Invalid email notification parameters")
        send_email(
            recipient_email=follower_email,
            subject=f"New music from {author_name}",
            body=f"Dear user,\n\nNew music '{music_name}' from {author_name} is now available!"
        )
    except Exception as e:
        print(f"Failed to send email to {follower_email}: {e}")
