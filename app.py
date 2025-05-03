#!flask/bin/python
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from usersGroups.urls import user_router, group_router
from spendings.urls import router as spendings_router

load_dotenv()

app = FastAPI(redirect_slashes=False)

origins = [
    "http://localhost",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:5173",
    "http://localhost:5174",
    "https://insola-design.ru",
    "https://layout.insola.tech",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(group_router)
app.include_router(spendings_router)

# CORS(app, origins=['http://localhost:3000', 'https://verni-sotku-8fyod.ondigitalocean.app'])
#
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#
# SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
# RANGE_NAME = os.environ['RANGE_NAME']
#
# def get_credentials():
#     creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
#
#     return creds
#
# @app.route('/')
# def index():
#     return "Hello, World!"
#
# @app.route('/all-rows')
# def get_all_rows():
#     gc.collect()
#     try:
#         service = build('sheets', 'v4', credentials=get_credentials())
#         sheet = service.spreadsheets()
#         result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                                     range=RANGE_NAME).execute()
#         values = result.get('values', [])
#         if not values:
#             print('No data found.')
#             return []
#
#         return values
#     except HttpError as err:
#         print(err)
#         abort(500)
#
# @app.route('/add-spending', methods=['POST'])
# def add_spending():
#     gc.collect()
#     data = json.loads(request.data.decode('utf-8'))
#     if not data or not 'spending' in data:
#         abort(400)
#
#     req_body = {
#         "range": RANGE_NAME,
#         "majorDimension": 'ROWS',
#         "values": [
#             [
#                 data['spending']['who'],
#                 data['spending']['whom'],
#                 data['spending']['sum'],
#                 data['spending']['comment']
#             ]
#         ]
#     }
#
#     try:
#         service = build('sheets', 'v4', credentials=get_credentials())
#         sheet = service.spreadsheets()
#         result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
#                                        range=RANGE_NAME,
#                                        valueInputOption='USER_ENTERED',
#                                        insertDataOption='INSERT_ROWS',
#                                        body=req_body).execute()
#
#         return result
#     except HttpError as err:
#         print(err)
#         return []
#
# @app.route('/statistics', methods=['GET'])
# def get_statistics():
#     values = []
#     try:
#         service = build('sheets', 'v4', credentials=get_credentials())
#         sheet = service.spreadsheets()
#         result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                                     range=RANGE_NAME).execute()
#         values = result.get('values', [])
#
#     except HttpError as err:
#         print(err)
#         return []
#
#     stats = {} # словарь объектов с ключами вида кто->кому и значениями в виде словаря кто,кому,сумма
#     response = {}
#     people = set(['Антон', 'Эльнур', 'Рома', 'Лера', 'Всем'])
#     people_except_all = set(['Антон', 'Эльнур', 'Рома', 'Лера'])
#
#     for person_a in people:
#         for person_b in people:
#             if person_a == person_b:
#                 continue
#
#             if person_a not in stats:
#                 stats[person_a] = {}
#
#             if person_b not in stats:
#                 stats[person_b] = {}
#
#             if person_b not in stats[person_a]:
#                 stats[person_a][person_b] = {
#                     "who_owes": person_a,
#                     "whom_owes": person_b,
#                     "sum": 0,
#                 }
#
#             if person_a not in stats[person_b]:
#                 stats[person_b][person_a] = {
#                 "who_owes": person_b,
#                 "whom_owes": person_a,
#                 "sum": 0,
#             }
#
#     for val in values[1:]:
#         whom_owes = val[0]
#         who_owes = val[1]
#         sum = float(re.sub(",", "", val[2].split(' ')[0]))
#
#         stats[who_owes][whom_owes]["sum"] += sum
#
#     for person_a in people_except_all:
#         for person_b in people_except_all:
#             if person_b == person_a:
#                 continue
#             stats[person_a][person_b]["sum"] += stats["Всем"][person_b]["sum"] / 4
#
#     del stats["Всем"]
#
#     response_data = {
#         "summed": stats,
#         "non_summed": copy.deepcopy(stats)
#     }
#
#     for person_a in people_except_all:
#         for person_b in people_except_all:
#             if person_b == person_a:
#                 continue
#
#             person_a_owes_to_b = response_data["summed"][person_a][person_b]
#             person_b_owes_to_a = response_data["summed"][person_b][person_a]
#             if person_a_owes_to_b["sum"] > person_b_owes_to_a["sum"]:
#                 person_a_owes_to_b["sum"] = person_a_owes_to_b["sum"] - person_b_owes_to_a["sum"]
#                 person_b_owes_to_a["sum"] = 0
#             else:
#                 person_b_owes_to_a["sum"] = person_b_owes_to_a["sum"] - person_a_owes_to_b["sum"]
#                 person_a_owes_to_b["sum"] = 0
#
#     return response_data
#
# @app.route('/get-users', methods=['GET'])
# def get_users_route():
#     return get_users()
#
# @app.route('/add-user', methods=['POST'])
# def add_user():
#     data = json.loads(request.data.decode('utf-8'))
#     if not data or not 'user' in data:
#         abort(400)
#
#     return create_user(data['user']['uuid'],data['user']['name'],data['user']['email'])
#
# @app.route('/get-user/<uuid>', methods=['GET'])
# def get_user_route(uuid):
#     user = get_user_by_uuid(uuid)
#     return user or []
#
# @app.route('/add-group', methods=['POST'])
# def add_group_route():
#     data = json.loads(request.data.decode('utf-8'))
#     if not data or not 'group' in data:
#         abort(400)
#
#     return create_group(data['group']['name'], data['group']['uuid'])
#
#
# @app.route('/get-groups/<user_uuid>')
# def get_all_user_groups_route(user_uuid):
#     return get_all_user_groups(user_uuid)
#
#
# @app.route('/get-group/<slug>')
# def get_group_by_slug_route(slug):
#     return get_group_by_slug(slug)
#
# if __name__ == '__main__':
#     app.run(debug=True)
