import mysql.connector

conexion = mysql.connector.connect(
    host="bq5khnloapqqfal7sr8u-mysql.services.clever-cloud.com",
    user="ug5aqugn1mlfkljc",
    password="fVbvJJnAybtXVb7ekEp6",
    database="bq5khnloapqqfal7sr8u"
)

cnx = mysql.connector.connect(**config)    
cursor = cnx.cursor()

