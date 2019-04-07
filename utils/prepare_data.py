import os
import gzip
import json
import nltk
import numpy as np
import pandas as pd
from tqdm import tqdm


HOME_DIR = os.environ['HOME_DIR']
DATA_DIR = f'{HOME_DIR}data/zen/'


def utf8_preview(d):
    try:
        return d.apply(lambda x: x.decode("utf8"))
    except:
        return d


def split_ratings(user_items, user_ratings, train_size=0.8):
    user_feedback = list(zip(user_items, user_ratings))
    user_feedback_1 = list(filter(lambda x: x[1] != 0, user_feedback))
    user_feedback_0 = list(filter(lambda x: x[1] == 0, user_feedback))

    split_1_n = int(len(user_feedback_1) * train_size)
    split_0_n = int(len(user_feedback_0) * train_size)
    user_feedback_train = user_feedback_1[:split_1_n] + user_feedback_0[:split_0_n]
    user_feedback_test = user_feedback_1[split_1_n:] + user_feedback_0[split_0_n:]
    return list(zip(*user_feedback_train)), list(zip(*user_feedback_test))


image_size = 96
def get_zen_data(train_size=0.8):
    # load items
    items_df = []
    for line in tqdm(gzip.GzipFile(f"{DATA_DIR}items.json.gz", "r"), 'loading items'):
        j = json.loads(line)
        j["content"] = j["content"].encode("utf8")  # storing in utf8 saves RAM
        j["title"] = j["title"].encode("utf8")
        if np.isnan(j["image"]).any():
            j["image"] = [0]*image_size
        items_df.append(j)
    items_df = pd.DataFrame(items_df).apply(utf8_preview)

    # load users and split on train and test
    users_train_df, users_test_df = [], []
    for line in tqdm(gzip.GzipFile(f"{DATA_DIR}train.json.gz", "r"), 'loading users'):
        j = json.loads(line)
        user_items = []
        user_ratings = []
        for item, rating in j["trainRatings"].items():
            user_items.append(int(item))
            user_ratings.append(int(rating))

        user_train, user_test = split_ratings(user_items, user_ratings)
        users_train_df.append({
            'userId': j["userId"],
            'userItems': np.array(user_train[0]),
            'userRatings': np.array(user_train[1]),
        })
        users_test_df.append({
            'userId': j["userId"],
            'userItems': np.array(user_test[0]),
            'userRatings': np.array(user_test[1]),
        })
    users_train_df = pd.DataFrame(users_train_df)
    users_test_df = pd.DataFrame(users_test_df)
    return items_df, (users_train_df, users_test_df)


from gensim.models.doc2vec import TaggedDocument
tokenizer = nltk.tokenize.WordPunctTokenizer()


def tokenize(text):
    return [t for t in tokenizer.tokenize(text.lower()) if len(t) >= 2]


class zen_text_iterator:
    def __init__(self, sampling_rate=1.0):
        self.sampling_rate = sampling_rate

    def __iter__(self):
        for line in gzip.GzipFile(f"{DATA_DIR}items.json.gz", "r"):
            if np.random.random() > self.sampling_rate:
                continue
            j = json.loads(line)
            text = j["title"] + " " + j["content"]
            yield TaggedDocument(tokenize(text), [j["itemId"]])


if __name__ == "__main__":
    items_df, (train_df, test_df) = get_zen_data()
