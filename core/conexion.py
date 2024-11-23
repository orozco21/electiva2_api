import mysql.connector

config = {
    host="bq5khnloapqqfal7sr8u-mysql.services.clever-cloud.com",
    user="ug5aqugn1mlfkljc",
    password="fVbvJJnAybtXVb7ekEp6",
    database="bq5khnloapqqfal7sr8u"
    'raise_on_warnings': True,}

cnx = mysql.connector.connect(**config)    
cursor = cnx.cursor()

