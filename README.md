# Reddit_extractor_mail_sender

Send the reddit post you want to your email!
=============================================

*Requirements: Python 3.8+, Praw, google-api-python-client google-auth-httplib2 google-auth-oauthlib*

If you want add a database I will show examples with mongodb (so install pymongo, but if you will use a server should install pymongo[srv])

You may have trouble installing google requirements and pymongo[srv], if you have trouble try:

```Python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pymongo[srv]
```
# FAQ

### Can I add a database to my project?

Yes, you can. I use mongodb in this example, but you can use other db. If you will use mongodb too, You should edit  “collectionname” inside [database.py](http://database.py).

```Python
"""
Well, in this example I only store submission.id to get already sent posts in subreddit
and Already created unique and ttl indexes via mongosh 
"""

import praw
import os
from datetime import datetime
from dotenv import load_dotenv
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
#Check if your connection with mongodb works
check_connection = check_mongo_connection(os.getenv(''))

for submission in reddit.subreddit('name of subreddit').new():  
    #Create a variable that check if index already exist inside collection
	check_if_exist = db.posts.find_one({'id': submission.id})
		if not check_if_exist:
		"""
		Insert id to check if exist in unique inside mongodb and 
		get date to delete when ttl index expire
		"""	
		db.collection.insert_many(
			[
				{
					'id': submission.id,
					'date': datetime.utcnow()
				}
			]	
		)
                           
		email_body = f'Sub: {submission.subreddit}\nTitle: {submission.title}\nLink: reddit.com/{submission.permalink}\n'
    		formated_string.append(email_body)
    
  if formated_string == []:
        print('Nothing to send')
        pass
  else:
        service = gmail_authenticate()
        send_message(service, '', '', '\n'.join(formated_string))
        print('Your email was sent!')
``` 
### How add sleep time in email function?

It’s simple, just create a condition and put logic inside

```Python
if sleep_time != 0:
        if formated_string == []:
           print('tem nada')
           pass
        else:
           service = gmail_authenticate()
           send_message(service, send_to, 'Posts reddit', '\n'.join(formated_string))
           print('Enviou')
           time.sleep(sleep_time)
```
### Is it possible have more than 1 sub?

Yes, but it is a bit trick, you have two options.

I recommend this one if you will use 3 or less subs:
```Python
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

for submission in reddit.subreddit("anime_irl+nier+sports").new():  
    email_body = f'Sub: {submission.subreddit}\nTitle: {submission.title}\nLink: reddit.com/{submission.permalink}\n'
    formated_string.append(email_body)
    
    if formated_string == []:
        print('Nothing to send')
        pass
    else:
        service = gmail_authenticate()
        send_message(service, send_to, '', '\n'.join(formated_string))
        print('Your email was sent!')

```
If you will use more than 3 you will need create a list and use a for, Idk why praw method doesn’t work with more than 3 subs.
```Python
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
sub_names = ['anime_irl', 'nier', 'sports', 'NBA2k']
send_to = os.getenv('')
formated_string = []

for subs in sub_names:
    for submission in reddit.subreddit(subs).new():  
        email_body = f'Sub: {submission.subreddit}\nTitle: {submission.title}\nLink: reddit.com/{submission.permalink}\n'
        formated_string.append(email_body)

        if formated_string == []:
            print('Nothing to send')
            pass
        else:
            service = gmail_authenticate()
            send_message(service, send_to, '', '\n'.join(formated_string))
            print('Your email was sent!')
```
