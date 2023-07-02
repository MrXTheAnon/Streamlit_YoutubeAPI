# Change file name to config.py
import mysql.connector
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Create Youtube API Key using your account
API_KEY = ''

# Create MongoDB account and Database, collection using your account
PYMONGO_URL = ''
PYMONGO_DB_NAME = ''
PYMONGO_COLLECTION_CHANNEL = ''
PYMONGO_COLLECTION_PLAYLIST = ''
PYMONGO_COLLECTION_VIDEO = ''
PYMONGO_COLLECTION_COMMENTS = ''

urlNotValidMsg = 'Given URL is not valid'
urlPresentMsg = 'Channel already present'

# SQL connection
def sqlConnection():
    myDB = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=PYMONGO_DB_NAME
    )

    return myDB, myDB.cursor(buffered=True)

# MongoDB connection
def mongoConnection():
    client = MongoClient(PYMONGO_URL, server_api=ServerApi('1'))

    # Using only one collection from mongodb since passing as one whole document(json).
    db = client[PYMONGO_DB_NAME][PYMONGO_COLLECTION_CHANNEL]

    return client, db
