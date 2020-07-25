from threading import Thread
from flask import Flask, request, redirect, make_response
from flask_cors import CORS
from werkzeug.serving import make_server
from http.server import HTTPServer
import requests
import urllib.parse
import json
import random
import string
import base64

cookie_key = 'spotify_auth_state'
client_id = ''
client_secret = ''
auth_string = f'{client_id}:{client_secret}'
redirect_uri = 'http://localhost:8365/callback'


# Ref: https://stackoverflow.com/a/45017691
class SpotifyAuthServer(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.app = Flask(__name__, static_folder='public')
        CORS(self.app)
        self.app.debug = False
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/login', 'login', self.login)
        self.app.add_url_rule('/callback', 'callback', self.callback)
        self.app.add_url_rule('/refresh_token', 'refresh_token', self.refresh_token)
        self.server: HTTPServer = make_server('127.0.0.1', 8365, self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.access_token = ''
        self.refresh_token = ''

    def run(self):
        self.server.serve_forever()

    def index(self):
        return self.app.send_static_file('index.html')

    def login(self):
        state = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))

        scope = 'user-modify-playback-state'
        query = {
             'response_type': 'code',
             'client_id': client_id,
             'scope': scope,
             'redirect_uri': redirect_uri,
             'state': state
        }
        response = make_response(
            redirect(f'https://accounts.spotify.com/authorize?{urllib.parse.urlencode(query)}')
        )
        response.set_cookie(cookie_key, state)
        return response

    def callback(self):
        code = request.args.get('code')
        state = request.args.get('state')
        stored_state = request.cookies.get(cookie_key)
        if state is None or state != stored_state:
            return 'state_mismatch'
        else:
            get_token_request = requests.post(
                url='https://accounts.spotify.com/api/token',
                data={
                    'code': code,
                    'redirect_uri': redirect_uri,
                    'grant_type': 'authorization_code'
                },
                headers={
                    'Authorization': 'Basic ' + base64.b64encode(auth_string.encode('ascii')).decode('ascii')
                }
            )
            if get_token_request.status_code == 200:
                body = json.loads(get_token_request.text)
                self.access_token, self.refresh_token = body['access_token'], body['refresh_token']
                response = make_response('noice')
                response.set_cookie(cookie_key, '')
                return response
            else:
                response = make_response('invalid_token')
                response.set_cookie(cookie_key, '')
                return response

    def refresh_token(self):
        get_new_token_request = requests.post(
            url='https://accounts.spotify.com/api/token',
            data={
                'refresh_token': request.args.get('refresh_token'),
                'grant_type': 'refresh_token'
            },
            headers={
                'Authorization': 'Basic ' + base64.b64encode(auth_string.encode('ascii')).decode('ascii')
            }
        )
        if get_new_token_request.status_code == 200:
            body = json.loads(get_new_token_request.text)
            self.access_token = body['access_token']
            return 'success'
        else:
            return 'failure'

    def shutdown(self):
        self.server.shutdown()
