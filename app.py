import flask
import os
from flask import jsonify
import time
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime
import pytz

app = flask.Flask(__name__)
#port = int(os.getenv("PORT", 9099))

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gs = gspread.authorize(creds)

tz = pytz.timezone('Asia/Kolkata')


@app.route('/')
def index():
        sheet = gs.open('Khel Khazana')
        user_details = sheet.get_worksheet(1).get_all_values()
        df = pd.DataFrame(user_details)
        df.columns = df.iloc[0]
        df = df[1:]
        table = df[['Name', 'Coins']].to_html().replace("dataframe", "w3-table-all w3-hoverable")
        return flask.render_template('index.html', table = table)

if __name__ == '__main__':
    app.run()
