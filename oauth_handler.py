import json
import requests

class Oauth_Handler:

    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.response_type = "code"
        self.redirect_uri = None
        self.access_url = None
        self.access_token = None

    def oauth_authorise(self):
        pass

    def oauth_access(self):
        pass

    