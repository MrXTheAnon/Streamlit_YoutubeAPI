# Youtube API with Streamlit, MongoDB, MySQL and Python.

### Description

Hello all, this is my first project using python for listing youtube channel details.

### Files

- **Streamlit**
- **Youtube**
- **MongoDb**
- **SQL**
- **NOTE**

### Workflow

This streamlit app contains single page with adding a channel details through custom url, where the channel response with playlist, videos, and comments are flattened and parsed to MongoDB Atlas server, and then retreiving the documents and  parsing to MySQL localhost.

It lists all the channel names in the select box which displays short details of the channel.

You can delete single or all records from both MongoDB and SQL.

And further some details have been added or queried from SQL to streamlit app.


### Streamlit

Here all the User Interface modules, designs and retreiving data from SQL has been done. All user inputs are given here.


### Youtube

Here every json responses are collected from channel, playlist, video, comment and it is flattened to required format and passed to MoongoDB Atlas server.

### MongoDb

Here all single and all documents are queried and deletes one or all documents.

### SQL

Here all single and all data are queried and deletes one or all data. 

### NOTE

In MySQL four seperate tables for channel, playlist, video, comments and interlinked with foreign keys with respective id's.

Please configure the required settings for connecting with Youtube, MongoDB, SQL.

This app still has some bugs or will return errors.
