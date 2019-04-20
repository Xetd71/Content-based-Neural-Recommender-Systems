import os
import numpy as np
import tensorflow as tf
from keras.models import load_model

HOME_DIR = os.environ['HOME_DIR']
PREPROC_DIR = f'{HOME_DIR}data/zen/preproc/'
PRETRAINED_MODELS_DIR = f'{HOME_DIR}pretrained_models/'


class KerasModel(object):
    def __init__(self, path):
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.session = tf.Session()
            with self.session.as_default():
                self.model = load_model(path)

    def predict(self, data):
        with self.graph.as_default():
            with self.session.as_default():
                return self.model.predict(data)


items_factors = np.load(f'{PRETRAINED_MODELS_DIR}als_model/items_factors.npy')
users_factors = np.load(f'{PRETRAINED_MODELS_DIR}als_model/users_factors.npy')
mlp_model = KerasModel(f'{PRETRAINED_MODELS_DIR}mlp_model/mlp_model')
dssm_model = KerasModel(f'{PRETRAINED_MODELS_DIR}dssm_model/dssm_model')
item_embeddings = np.load(f'{PREPROC_DIR}items_embeddings.npy')
users_embeddings = np.load(f'{PREPROC_DIR}users_embeddings.npy')


def __issue_recommendation(func):
    def recommend(user_id, unseen_item_ids, n=None):
        p = func(user_id, unseen_item_ids)
        return list(map(lambda x: x[1], sorted(zip(p, unseen_item_ids), key=lambda x: -x[0])))[:n]
    return recommend


@__issue_recommendation
def als_recommend(user_id, unseen_item_ids):
    return items_factors[unseen_item_ids].dot(users_factors[user_id])


@__issue_recommendation
def mlp_recommend(user_id, unseen_item_ids):
    return mlp_model.predict([
        np.full(len(unseen_item_ids), user_id),
        item_embeddings[unseen_item_ids]])


@__issue_recommendation
def dssm_recommend(user_id, unseen_item_ids):
    return dssm_model.predict([
        users_embeddings[np.full(len(unseen_item_ids), user_id)],
        item_embeddings[unseen_item_ids]])


# def __batch_predict(users, items, model, batch_size):
#     return np.concatenate(model.predict(
#         [users[idx:idx + batch_size], items[idx:idx + batch_size]])
#                           for idx in np.arange(0, len(users) - batch_size, batch_size))
#
#
# @__issue_recommendation
# def mlp_recommend(user_id, unseen_item_ids, batch_size=512):
#     return __batch_predict(
#         np.full(len(unseen_item_ids), user_id),
#         item_embeddings[unseen_item_ids],
#         mlp_model,
#         batch_size)
#
#
# @__issue_recommendation
# def dssm_recommend(user_id, unseen_item_ids, batch_size=512):
#     return __batch_predict(
#         users_embeddings[np.full(len(unseen_item_ids), user_id)],
#         item_embeddings[unseen_item_ids],
#         dssm_model,
#         batch_size)
