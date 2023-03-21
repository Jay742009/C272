import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC215e607ebedc5ea8fd6da53a5c48579f'
    TWILIO_SYNC_SERVICE_SID = 'ISf9ce549bf6f877a6a04b23192c17bfb1'
    TWILIO_API_KEY = 'SK8a3c085d6318f47d23dbdcd590275407'
    TWILIO_API_SECRET = 'aEU0cejW4HmtSAo9e3yYYtL2I5HvpXlH'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    
    with open('writefile.txt','w') as f:
    	f.write(text_from_notepad)

    path_to_store_text = 'writefile.txt'
    
    return send_file(path_to_store_text,as_attachment=True)
    
if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
