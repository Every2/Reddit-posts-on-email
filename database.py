from pymongo import MongoClient 
from dotenv import load_dotenv
import os
from pymongo.errors import ServerSelectionTimeoutError

load_dotenv()

def check_mongo_connection(client_uri: str) -> None:
    """_summary_
    Check if your connection is working if not send an error
    Args:
        client_uri (str): pass your client uri and function will check
    """
    client = MongoClient(client_uri)

    try:
        client.list_database_names()
        print('Connected')
        

    except ServerSelectionTimeoutError as err:
        print(f"Data Base Connection failed. Error: {err}")
        

   
client = MongoClient(os.getenv(''))
#Change collectionname to name of your collection
db = client.collectionname



