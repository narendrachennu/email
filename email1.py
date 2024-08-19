#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import json


# In[2]:


with open('config.json') as config_file:
    config= json.load(config_file)
    
# Your email credentials
#sender_email = "your_email@gmail.com"
#password = "your_password"
recipients_email = ["2631narendra@gmail.com"]
sender_email = config['email_user']
subject = "Subject of the Email"
body = """
Hello,

This is a test email sent from Python script.

Best regards,
narendra
"""


# In[3]:


smtp_server = "smtp.gmail.com"
port = 587

def send_email(recipients_email, sender_email, config, subject, body, attachment_path=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipients_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            filename = os.path.basename(attachment_path)
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={filename}',
                )
                msg.attach(part)

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(config['email_user'], config['email_pass'])

        # Send the email
        server.sendmail(sender_email, recipients_email, msg.as_string())

        # Disconnect from the server
        server.quit()

        print(f"Email successfully sent to {recipients_email}")

    except Exception as e:
        print(f"Error sending email to {recipients_email}: {e}")


# In[4]:


# Path to the attachment (if any)
attachment_path = r"dcda549c37b49138a8b245a5177a3aeb.jpg"

# Send email to each recipient
for recipient in recipients_email:
    send_email(recipient, sender_email, config, subject, body, attachment_path)


# In[5]:


# Streamlit app
st.title('Email Sender App with Attachment')

st.sidebar.header('Email Configuration')
smtp_server = st.sidebar.text_input('SMTP Server', 'smtp.gmail.com')
smtp_port = st.sidebar.number_input('SMTP Port', 587)
login = st.sidebar.text_input('Login Email')
password = st.sidebar.text_input('Password', type='password')

st.header('Compose Email')
sender_email = st.text_input('Sender Email', login)
receiver_email = st.text_input('Receiver Email')
subject = st.text_input('Subject')
message = st.text_area('Message')
attachment = st.file_uploader("Choose a file", type=["txt", "pdf", "png", "jpg", "jpeg", "gif", "docx", "xlsx"])


# In[6]:


if st.button('Send Email'):
    result = send_email(sender_email, receiver_email, subject, message, smtp_server, smtp_port, login, password, attachment)
st.write(result)


# In[ ]:




