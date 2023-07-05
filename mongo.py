from pymongo import MongoClient

import os
#
print("start connection with mongo file")

# db connection
client = MongoClient(os.getenv("DB_URL"))
# define db_name as "fastapiDB"
db = client["grapheneDB"]
# define table_name as "person"
collection = db["person"]
# class