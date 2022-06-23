import praw
import time
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

sub_name = []
sub_tags = []
last_ids = []
sleep_time = 0

verification = check_mongo_connection(os.getenv(''))   

while True:
    posts = []
    for subs in sub_name:
        for tag in sub_tags:
            for submission in reddit.subreddit(subs).new():  
                post = db.posts.find_one({'id': submission.id})  
                
                if not submission.id in last_ids:
                    lower_case_title = str.lower(submission.title) 
                    
                    if 'forhire' in lower_case_title or 'for hire' in lower_case:        
                        pass
                    
                    elif tag in lower_case_title:                            
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
                            posts.append(result)
                            last_ids.append(submission.id)
                                               
    if sleep_time != 0:
        if posts == []:
           print('Nothing to send')
           pass
        else:
           service = gmail_authenticate()
           send_message(service, '', '', '')
           print('Your email was sent!')
           time.sleep(sleep_time)
      
