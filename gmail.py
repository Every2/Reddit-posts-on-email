from inspect import Parameter
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from typing import NewType

#Call a function as a parameter
callabe = NewType('callabe', Parameter)


SCOPES = ['https://mail.google.com/']
our_email = os.getenv('mail')

def gmail_authenticate() -> str:
    creds = None
    """_summary_
    When you do login one time token.pickle will store access and refresh tokens
    to automatically login without request everytime you run your script.
    Returns:
        str: Return gmail, v1 and credentials to your token.pickle.
    """
    
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def build_message(destination: str, obj: str, body: str) -> dict:
    """_summary_
    Create content of email
    Args:
        destination (str): To who you want send email
        obj (str): Subject of email
        body (str): Content of email

    Returns:
        dict: Use mime to send email and b64 to avoid problems with gmail protocols
    """
    message = MIMEText(body)
    message['to'] = destination
    message['from'] = our_email
    message['subject'] = obj
    
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service: callabe, destination: str, subject: str, body:str) -> callabe:
    """_summary_
    Send message calling authentification and call gmail_authenticate and build_message to send email via gmail api
    Args:
        service (callabe): A parameter that call gmail_authenticate function, you should create a variable that call gmail_authenticate and put here
        destination (str): To who you want send email
        subject (str): Subject of email
        body (str): Content of email

    Returns:
        callabe: send email with api using build_message function
    """
    return service.users().messages().send(
      userId="me",
      body=build_message(destination, subject, body)
    ).execute()


