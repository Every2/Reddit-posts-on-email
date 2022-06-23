import praw
import os
from dotenv import load_dotenv
from datetime import datetime
from gmail import send_message, gmail_authenticate 
from database import db, check_mongo_connection

load_dotenv()

reddit = praw.Reddit(
    client_id= os.getenv(''),
    client_secret= os.getenv(''),
    user_agent= os.getenv(''),
)

send_to = os.getenv('')
formated_string = []

verification = check_mongo_connection(os.getenv(''))   

for submission in reddit.subreddit('name of subreddit').new():  
    post = db.posts.find_one({'id': submission.id})               
    if not post:
        db.posts.insert_many(
            [
                {
                    'id': submission.id,
                    'date': datetime.utcnow()
                }
            ]
        )
        result = f'Sub: {submission.subreddit}\nTitle: {submission.title}\nLink: reddit.com/{submission.permalink}\n'
        formated_string.append(result)
            
    
    if formated_string == []:
        print('Nothing to send')
        pass
    else:
        service = gmail_authenticate()
        send_message(service, '', '', '')
        print('Your email was sent!')
        
                            
                                               
    
