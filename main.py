# * Import Python Module
import certifi
from flask import Flask
from mongoengine import connect

# * Import User Defined Functions
from app.routes.chatbotCRUD import chatbot_user_module
from app.routes.patientCRUD import patient_module
from app.routes.login import login_module
from app.routes.chatbotResponseCRUD import chatbot_response_module
from app.routes.medicalRecordCRUD import medicalrecord_module

from config import host_uri

# * Initialize Flask API
app = Flask(__name__)


# * Initialize Base Flask API
@app.route("/")
def hello_world():
    return "Hello, User!"


app.register_blueprint(chatbot_user_module, url_prefix="/users")
app.register_blueprint(patient_module, url_prefix="/patient")
app.register_blueprint(login_module)
app.register_blueprint(chatbot_response_module, url_prefix="/chatbot-response")
app.register_blueprint(medicalrecord_module, url_prefix="/medical-record")

# Define the MongoDB connection
connect(
    host=host_uri,
    tlsCAFile=certifi.where(),
)


# * Run API Server
if __name__ == "__main__":
    # run_server()
    app.run(debug=True)
