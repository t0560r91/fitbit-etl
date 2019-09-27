import flask 
import json 
import requests
import base64
import os


with open('var/creds/app-creds.json', 'r') as f:
    app_creds = json.load(f)


client_id = app_creds['client_id']
client_secret = app_creds['client_secret']
encoded_client_cred = base64.b64encode(bytes(f'{client_id}:{client_secret}', 'utf'))



app = flask.Flask(__name__, static_url_path='')



@app.route('/')
def home():
    # get code
    try:
        code = flask.request.query_string.decode('utf-8')[5:]
        
        # request token
        url = "https://api.fitbit.com/oauth2/token"
        headers = {
            'content-type' : 'application/x-www-form-urlencoded', 
            'authorization' : 'Basic ' + encoded_client_cred.decode('utf')
            }
        data = f'client_id={client_id}&grant_type=authorization_code&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000&code={code}'
        token = json.loads(requests.post(url, headers=headers, data=data).text)

        # export token
        if 'tokens' not in os.listdir('var'): os.mkdir('var/tokens/')
        with open('var/user_id.txt', 'r') as f:
            user_id = f.read()
        with open(f'var/tokens/token_{user_id}.json', 'w') as f:
            json.dump(token, f)
        return flask.jsonify(token)
        
    except:
        return 'heller'        




