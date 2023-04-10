# * Import Python Module
import certifi
from flask import Flask
from mongoengine import connect

# * Import User Defined Functions
from app.routes.chatbotCRUD import chatbot_user_module
from app.routes.patientCRUD import patient_module
from app.routes.chatbotResponseCRUD import chatbot_response_module
from config import host_uri

# * Initialize Flask API
app = Flask(__name__)
app.register_blueprint(chatbot_user_module, url_prefix="/users")
app.register_blueprint(patient_module, url_prefix="/patient")
app.register_blueprint(chatbot_response_module, url_prefix="/chatbot-response")

# Define the MongoDB connection
connect(
    host=host_uri,
    tlsCAFile=certifi.where(),
)


# * Run API Server
if __name__ == "__main__":
    # run_server()
    app.run(debug=True)
