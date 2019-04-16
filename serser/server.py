import os
import sys
import pandas as pd
import numpy as np
from flask import Flask
from flask import jsonify

app = Flask(__name__)


IS_LOCAL = True
HOME_DIR = ('/mnt/E/Projects/' if IS_LOCAL else '/home/Xetd71/') + 'Content-based-Neural-Recommender-Systems/'
os.environ['HOME_DIR'] = HOME_DIR

sys.path.append("..")

from utils.prepare_data import zen

DATA_DIR = f'{HOME_DIR}data/zen/'
PREPROC_DIR = f'{DATA_DIR}preproc/'


items_df = zen.items_df()
user_items = zen.user_items()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/user_items/<user_id>')
def show_user_items(user_id):
    items = items_df.iloc[user_items[user_id]]
    return jsonify(items)


# @app.route('/als/<user_id>')
# def show_als_recommendation(user_id):
#     items = items_df.iloc[als.predict(user_id)]
#     return jsonify(items)
