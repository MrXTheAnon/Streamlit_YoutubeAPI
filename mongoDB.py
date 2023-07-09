import streamlit as st
from config import mongoConnection
from sqlDB import ytSqlAddData

client, db = mongoConnection()
def mongoFind():
    client, db = mongoConnection()
    cursor = db.find()
    return (
        'Empty Document'
        if cursor == ''
        else [
            document['Channel_Name']['Channel_Id'] for document in cursor
        ]
    )

def mongoAdd(jsonResponse):

    mongoFindResp = mongoFind()

    if jsonResponse['Channel_Name']['Channel_Id'] in mongoFindResp:
        return "Doc already present"
    document = [jsonResponse]
    db.insert_one(document)
    # db.insert_many(document) # TODO : Check the condition insertone is working or not.
    ytSqlAddData(jsonResponse=jsonResponse)
        
    # client.close()

def mongoDelOne(delId):
    db.delete_one({"Channel_Name.Channel_Id" : delId})
    # client.close()

def mongoDelAll():
    db.delete_many({})
    # client.close()