import praw
import time
import os
from dotenv import load_dotenv
from datetime import datetime
from gmail import send_message, gmail_authenticate 
from database import db, check_mongo_connection

load_dotenv()

reddit = praw.Reddit(
    client_id= os.getenv('ids'),
    client_secret= os.getenv('secret'),
    user_agent= os.getenv('agent'),
)

email_login = os.getenv('mail')
send_to = os.getenv('send')

sub_name = ['artcommissions', 'artisthirecommission', 'comissions', 'dndcommissions', 'hireanartist', 'HungryArtists']
sub_tags = ['looking', '[hiring]', 'my character', 'my oc']
last_ids = []
sleep_time = 3600

verification = check_mongo_connection(os.getenv('credentials'))   

while True:
    posts = []
    for subs in sub_name:
        for tag in sub_tags:
            for submission in reddit.subreddit(subs).new():  
                post = db.posts.find_one({'id': submission.id})  
                
                if not submission.id in last_ids:
                    lower_case = str.lower(submission.title) 
                    
                    if 'forhire' in lower_case or 'for hire' in lower_case:        
                        pass
                    
                    elif tag in lower_case:                            
                        if not post:
                            db.posts.insert_many(
                                [
                                    {
                                        'id': submission.id,
                                        'date': datetime.utcnow()
                                    }
                                ]
                            )
                            result = f'Sub: {submission.subreddit}\nTitulo: {submission.title}\nLink: reddit.com/{submission.permalink}\n'
                            posts.append(result)
                            last_ids.append(submission.id)
                            
                        
    if sleep_time != 0:
        if posts == []:
           print('tem nada')
           pass
        else:
           service = gmail_authenticate()
           send_message(service, send_to, 'Posts reddit', '\n'.join(posts))
           print('Enviou')
           time.sleep(sleep_time)

    

 
        
 
 

       