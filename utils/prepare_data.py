import os
import gzip
import json
import nltk
import numpy as np
import pandas as pd
from tqdm import tqdm
from gensim.models.doc2vec import TaggedDocument

tokenizer = nltk.tokenize.WordPunctTokenizer()

HOME_DIR = os.environ['HOME_DIR']
DATA_DIR = f'{HOME_DIR}data/zen/'
ZEN_IMAGE_SIZE = 96

def tokenize(text):
        return [t for t in tokenizer.tokenize(text.lower()) if len(t) >= 2]

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


class zen:
    train_size = 0.8

    @staticmethod
    def items():
        for line in tqdm(gzip.GzipFile(f"{DATA_DIR}items.json.gz", "r"), 'loading items'):
            j = json.loads(line)
            j["content"] = j["content"].encode("utf8")  # storing in utf8 saves RAM
            j["title"] = j["title"].encode("utf8")
            if np.isnan(j["image"]).any():
                j["image"] = [0] * ZEN_IMAGE_SIZE
            yield j

    @staticmethod
    def items_df():
        return pd.DataFrame(zen.items()).apply(utf8_preview)

    @staticmethod
    def users():
        for line in tqdm(gzip.GzipFile(f"{DATA_DIR}train.json.gz", "r"), 'loading users'):
            j = json.loads(line)
            user_items = []
            user_ratings = []
            for item, rating in j["trainRatings"].items():
                user_items.append(int(item))
                user_ratings.append(int(rating))

            yield {
                'userId': j["userId"],
                'userItems': np.array(user_items),
                'userRatings': np.array(user_ratings),
            }

    @staticmethod
    def users_df():
        return pd.DataFrame(zen.users())

    @staticmethod
    def user_items(n=None, shuffle=True):
        if shuffle:
            def select_func(user):
                items = user['userItems'][user['userRatings'] == 1]
                np.random.shuffle(items)
                return items[:n]
            return list(map(select_func, zen.users()))
        return list(map(lambda user: user['userItems'][user['userRatings'] == 1][:n], zen.users()))

    @staticmethod
    def __split_user(user):
        user_train, user_test = split_ratings(user['userItems'], user['userRatings'], zen.train_size)
        return {'userId': user["userId"],
                'userItems': np.array(user_train[0]),
                'userRatings': np.array(user_train[1])}, \
               {'userId': user["userId"],
                'userItems': np.array(user_test[0]),
                'userRatings': np.array(user_test[1])}

    @staticmethod
    def data():
        # load items
        items_df = zen.items()

        # load users and split on train and test
        users_train_df, users_test_df = zip(*map(zen.__split_user, zen.users()))
        users_train_df = pd.DataFrame(users_train_df)
        users_test_df = pd.DataFrame(users_test_df)
        return items_df, (users_train_df, users_test_df)

    class text_iterator:
        def __init__(self, title=True, content=True):
            self.title = title
            self.content = content
            if not title * content:
                raise AttributeError("title and content can't be False at the same time")

        def __iter__(self):
            for line in gzip.GzipFile(f"{DATA_DIR}items.json.gz", "r"):
                j = json.loads(line)
                text = "{} {}".format(j["title"] if self.title else "", j["content"] if self.content else "")
                yield TaggedDocument(tokenize(text), [j["itemId"]])


if __name__ == "__main__":
    pass
    # items_df, (train_df, test_df) = get_zen_data()
