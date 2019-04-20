import os
import sys
import pandas as pd
import numpy as np
from flask import Flask
from flask import jsonify
from flask import json

app = Flask(__name__)

IS_LOCAL = True
HOME_DIR = ('/mnt/E/Projects/' if IS_LOCAL else '/home/Xetd71/') + 'Content-based-Neural-Recommender-Systems/'
os.environ['HOME_DIR'] = HOME_DIR

sys.path.append("..")

from utils.prepare_data import zen
from zen_models_api import als_recommend, mlp_recommend, dssm_recommend

DATA_DIR = f'{HOME_DIR}data/zen/'
PREPROC_DIR = f'{DATA_DIR}preproc/'

ITEMS_TO_RECOMMEND = 20
items_df = zen.items_df()
user_items, unseen_items = zen.user_items(50)


@app.route('/')
def hello_world():
    return 'Content-based Neural Recommender System server'


@app.route('/user_items/<user_id>')
def show_user_items(user_id):
    items = items_df.iloc[user_items[int(user_id)]].to_json(orient='records')
    return jsonify(json.loads(items))


@app.route('/ALS/<user_id>')
def show_als_recommendation(user_id):
    items = items_df.iloc[als_recommend(int(user_id), unseen_items[int(user_id)], ITEMS_TO_RECOMMEND)].to_json(orient='records')
    return jsonify(json.loads(items))


@app.route('/MLP/<user_id>')
def show_mlp_recommendation(user_id):
    items = items_df.iloc[mlp_recommend(int(user_id), unseen_items[int(user_id)], ITEMS_TO_RECOMMEND)].to_json(orient='records')
    return jsonify(json.loads(items))


@app.route('/DSSM/<user_id>')
def show_dssm_recommendation(user_id):
    items = items_df.iloc[dssm_recommend(int(user_id), unseen_items[int(user_id)], ITEMS_TO_RECOMMEND)].to_json(orient='records')
    return jsonify(json.loads(items))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
