#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask_cors import CORS

import os
import json

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, origins=['http://localhost:3000', 'https://starfish-app-3hf2q.ondigitalocean.app/'])

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
RANGE_NAME = os.environ['RANGE_NAME']

def get_credentials():
    creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

    return creds

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/all-rows')
def get_all_rows():
    try:
        service = build('sheets', 'v4', credentials=get_credentials())
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
            return []

        return values
    except HttpError as err:
        print(err)
        return []

@app.route('/add-spending', methods=['POST'])
def add_spending():
    data = json.loads(request.data.decode('utf-8'))
    if not data or not 'spending' in data:
        abort(400)

    req_body = {
        "range": RANGE_NAME,
        "majorDimension": 'ROWS',
        "values": [
            [
                data['spending']['who'],
                data['spending']['whom'],
                data['spending']['sum'],
                data['spending']['comment']
            ]
        ]
    }

    try:
        service = build('sheets', 'v4', credentials=get_credentials())
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                                       range=RANGE_NAME,
                                       valueInputOption='USER_ENTERED',
                                       insertDataOption='INSERT_ROWS',
                                       body=req_body).execute()

        return result
    except HttpError as err:
        print(err)
        return []

if __name__ == '__main__':
    app.run(debug=True)