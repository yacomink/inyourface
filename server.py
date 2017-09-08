from oauth2client.client import GoogleCredentials
from flask import Flask
import httplib2
app = Flask(__name__)

@app.route("/")
def hello():
    credentials = GoogleCredentials.get_application_default()
    credentials.authorize(httplib2.Http())
    return "Authed against google!"

