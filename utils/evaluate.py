import os
import numpy as np
import pandas as pd
from tqdm import tqdm


HOME_DIR = os.environ['HOME_DIR']
DATA_DIR = f'{HOME_DIR}data/zen/'


def dcg_at_k(r, k=20, method=0):
    """
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        k: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
    Returns:
        Discounted cumulative gain
    """
    r = np.asfarray(r)[:k]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
        else:
            raise ValueError('method must be 0 or 1.')
    return 0.


def ndcg_at_k(r, k=20, method=0):
    """
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        k: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
    Returns:
        Normalized discounted cumulative gain
    """
    dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)
    if not dcg_max:
        return 0.
    return dcg_at_k(r, k, method) / dcg_max


class test:
    solution = pd.read_csv(f'{DATA_DIR}/solution.csv')
    ratings = {}
    user_items = {}
    user_ids = set(solution['userId'])
    for uid in tqdm(user_ids):
        uid_items = solution[solution['userId'] == uid]
        user_items[uid] = uid_items['itemId'].tolist()
        ratings[uid] = dict(zip(uid_items['itemId'], uid_items['rating']))

    @staticmethod
    def user_ndcg(user_id, ordered_items, k=20, method=1):
        true_ratings = test.ratings[user_id]
        return ndcg_at_k(list(map(lambda x: true_ratings[x], ordered_items)), k, method)

    @staticmethod
    def ndcg(predict, k=20, method=1):
        ndcg = 0
        for uid, items in tqdm(test.user_items.items()):
            ndcg += test.user_ndcg(
                uid,
                np.array(sorted(
                    zip(predict(uid, items), items),
                    key=lambda x: x[0],
                    reverse=True))[:, 1],
                k, method
            )
        return ndcg / len(test.user_items)


if __name__ == "__main__":
    click_rate_submission = pd.read_csv(f'{DATA_DIR}/click_rate_submission.csv')
    
    
    def predict(uid, items):
        predicted_order = click_rate_submission[click_rate_submission['userId'] == uid]['itemId'].values
        predicted_order = dict(zip(predicted_order, np.arange(predicted_order.shape[0], 0, -1)))
        return list(map(lambda x: predicted_order[x], items))
    
    
    test.ndcg(predict)
