from google.oauth2 import id_token
from google.auth.transport import requests
import os

request = requests.Request()

def verify_token_from_google(token):
    id_info = id_token.verify_oauth2_token(
        token, request, os.environ['GOOGLE_CLIENT_ID'])

    userid = id_info['sub']
    return id_info