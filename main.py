from flask import Flask
from app.routes.chatbotCRUD import chatbot_user_module

app = Flask(__name__)
app.register_blueprint(chatbot_user_module)
# Configure the MongoDB connection
app.config["MONGODB_SETTINGS"] = {
    "db": "chatbot",
    "host": "medicalanalysissystem.mptbxix.mongodb.net",
    "port": 27017,
    "username": "medadmin",
    "password": "hMna4RYKa0rIS9wp",
}


import os
from mongoengine import connect

#  Read key-value pairs from a .env file and set them as environment variables
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DATABASE_NAME")
host = os.getenv("DB_HOST")

# # Connecting to MongoDB
# host = f"mongodb://{user}:{password}@{host}/{database_name}"
# # mongodb+srv://<username>:<password>@cluster0.nxdac.mongodb.net/test
# print("Connecting to MongoDB ", host)
# db_connected = connect(host=host)


# Connecting to MongoDB
host = f"mongodb://{user}:{password}@{host}/{database_name}?ssl=true&ssl_cert_reqs=CERT_NONE"
print("Connecting to MongoDB ", host)

# host = f"mongodb+srv://{user}:{password}@cluster0.nxdac.mongodb.net/?retryWrites=true&w=majority"
# connect(host=host)
# Create the MongoDB connection
connect(**app.config["MONGODB_SETTINGS"])


if __name__ == "__main__":
    # run_server()
    app.run(debug=True)
