import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

base_url = 'https://example'
text_to_find = "example"

# You can put the same email here for simplicity
sender_email = "example@gmail.com"
receiver_email = 'example@gmail.com'

# For password, you're required to use app password. Take a look at that here: https://www.youtube.com/watch?v=Y_u5KIeXiVI
password = "password"

email_subject = "Subject Example"
email_body = "Body Example"

# Function to send email
def send_email():
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = email_subject
    body = email_body
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully!")

# Main function to check the webpage and possibly send an email
def check_page_and_notify():

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    found_element = soup.find('span', class_='highlight-text', text=text_to_find)

    if not found_element:
        send_email()
        return True  # Return True if the email was sent
    else:
        print("Text found, no need to send an email.")
        return False  # Return False if the text was found and no email was sent

email_sent = False  # Flag to keep track of whether the email has been sent

# Loop to continuously check the page every 1 minute until the email is sent
while not email_sent:
    email_sent = check_page_and_notify()
    if not email_sent:
        print("Waiting for 1 minute before checking again...")
        time.sleep(60)  # Sleep for 60 seconds
