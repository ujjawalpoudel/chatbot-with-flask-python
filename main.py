# * Import Python Module
import certifi
from flask import Flask
from mongoengine import connect

# * Import User Defined Functions
from app.routes.chatbotCRUD import chatbot_user_module
from config import host_uri

# * Initialize Flask API
app = Flask(__name__)
app.register_blueprint(chatbot_user_module, url_prefix="/users")


# Define the MongoDB connection
connect(
    host=host_uri,
    tlsCAFile=certifi.where(),
)


# * Run API Server
if __name__ == "__main__":
    # run_server()
    app.run(debug=True)
