#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask_cors import CORS

import os
import json
import gc
import re
import copy

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from db import get_db_connection

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, origins=['http://localhost:3000', 'https://starfish-app-3hf2q.ondigitalocean.app'])

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
    gc.collect()
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
        abort(500)

@app.route('/add-spending', methods=['POST'])
def add_spending():
    gc.collect()
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

@app.route('/statistics', methods=['GET'])
def get_statistics():
    values = []
    try:
        service = build('sheets', 'v4', credentials=get_credentials())
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

    except HttpError as err:
        print(err)
        return []

    stats = {} # словарь объектов с ключами вида кто->кому и значениями в виде словаря кто,кому,сумма
    response = {}
    people = set(['Антон', 'Эльнур', 'Рома', 'Лера', 'Всем'])
    people_except_all = set(['Антон', 'Эльнур', 'Рома', 'Лера'])

    for person_a in people:
        for person_b in people:
            if person_a == person_b:
                continue

            if person_a not in stats:
                stats[person_a] = {}

            if person_b not in stats:
                stats[person_b] = {}

            if person_b not in stats[person_a]:
                stats[person_a][person_b] = {
                    "who_owes": person_a,
                    "whom_owes": person_b,
                    "sum": 0,
                }

            if person_a not in stats[person_b]:
                stats[person_b][person_a] = {
                "who_owes": person_b,
                "whom_owes": person_a,
                "sum": 0,
            }

    for val in values[1:]:
        whom_owes = val[0]
        who_owes = val[1]
        sum = float(re.sub(",", "", val[2].split(' ')[0]))

        stats[who_owes][whom_owes]["sum"] += sum

    for person_a in people_except_all:
        for person_b in people_except_all:
            if person_b == person_a:
                continue
            stats[person_a][person_b]["sum"] += stats["Всем"][person_b]["sum"] / 4

    del stats["Всем"]

    response_data = {
        "summed": stats,
        "non_summed": copy.deepcopy(stats)
    }

    for person_a in people_except_all:
        for person_b in people_except_all:
            if person_b == person_a:
                continue

            person_a_owes_to_b = response_data["summed"][person_a][person_b]
            person_b_owes_to_a = response_data["summed"][person_b][person_a]
            if person_a_owes_to_b["sum"] > person_b_owes_to_a["sum"]:
                person_a_owes_to_b["sum"] = person_a_owes_to_b["sum"] - person_b_owes_to_a["sum"]
                person_b_owes_to_a["sum"] = 0
            else:
                person_b_owes_to_a["sum"] = person_b_owes_to_a["sum"] - person_a_owes_to_b["sum"]
                person_a_owes_to_b["sum"] = 0

    return response_data

@app.route('/get-users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    books = cur.fetchall()
    cur.close()
    conn.close()

    return books

@app.route('/add-user', methods=['POST'])
def add_user():
    data = json.loads(request.data.decode('utf-8'))
    if not data or not 'user' in data:
        abort(400)

    user = (
        data['user']['uuid'],
        data['user']['name'],
        data['user']['email']
    )

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('INSERT INTO users (uuid, name, email)'
                'VALUES (%s, %s, %s)',
                user)

    conn.commit()
    cur.close()
    conn.close()

    return []

if __name__ == '__main__':
    app.run(debug=True)