from pymongo import MongoClient 
from dotenv import load_dotenv
import os
from pymongo.errors import ServerSelectionTimeoutError

load_dotenv()

def check_mongo_connection(client_uri: str):
    """
    Check if your connection is valid, if it's return ok
    if not an error.
    """
    client = MongoClient(client_uri)

    try:
        client.list_database_names()
        print('Ok')
        

    except ServerSelectionTimeoutError as err:
        print(f"Data Base Connection failed. Error: {err}")
        

   
client = MongoClient(os.getenv('credentials'))
#Put our collection
db = client.collection_name



