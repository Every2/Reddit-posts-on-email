from pymongo import MongoClient 
from dotenv import load_dotenv
import os
from pymongo.errors import ServerSelectionTimeoutError

load_dotenv()

def check_mongo_connection(client_uri: str):
    client = MongoClient(client_uri)

    try:
        client.list_database_names()
        print('Ok')
        

    except ServerSelectionTimeoutError as err:
        print(f"Data Base Connection failed. Error: {err}")
        

   
client = MongoClient(os.getenv('credentials'))
db = client.collection_name



