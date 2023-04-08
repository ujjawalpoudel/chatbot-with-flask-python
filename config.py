import os
from mongoengine import connect

#  Read key-value pairs from a .env file and set them as environment variables
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DATABASE_NAME")
host = os.getenv("DB_HOST")

# Connecting to MongoDB
# host = f"mongodb://{user}:{password}@{host}/{database_name}"
# # mongodb+srv://<username>:<password>@cluster0.nxdac.mongodb.net/test
# print("Connecting to MongoDB ", host)
# db_connected = connect(host=host)
