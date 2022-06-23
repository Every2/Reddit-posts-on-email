import praw
import os
from dotenv import load_dotenv
from gmail import send_message, gmail_authenticate 

load_dotenv()

reddit = praw.Reddit(
    client_id= os.getenv(''),
    client_secret= os.getenv(''),
    user_agent= os.getenv(''),
)

send_to = os.getenv('')
formated_string = []

for submission in reddit.subreddit('name of subreddit').new():  
    email_body = f'Sub: {submission.subreddit}\nTitle: {submission.title}\nLink: reddit.com/{submission.permalink}\n'
    formated_string.append(result)
    
    if formated_string == []:
        print('Nothing to send')
        pass
    else:
        service = gmail_authenticate()
        send_message(service, '', '', '\n'.join(formated_string))
        print('Your email was sent!')
                                        
