import os
import numpy as np
import pandas as pd


def dcg_at_k(r, k, method=0):
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


def ndcg_at_k(r, k, method=0):
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


HOME_DIR = os.environ['HOME_DIR']
DATA_DIR = f'{HOME_DIR}data/zen/'
perfect_ranking = pd.read_csv(f'{DATA_DIR}/perfect_ranking.csv')
user_ids = set(perfect_ranking['userId'])


def zen_ndcg_at_k(user_id, user_items, k=20, method=0):
    if user_id in user_ids:
        item_rel = dict(zip(user_items, np.arange(user_items.shape[0] - 1, -1, -1)))
        perfect_order = perfect_ranking[perfect_ranking['userId'] == user_id]['itemId'].values
        return ndcg_at_k(list(map(lambda x: item_rel[x], perfect_order)), 20, method=1)
    return None


if __name__ == "__main__":
    print(ndcg_at_k([3, 2, 3, 0, 0, 1, 2, 2, 3, 0], 1, method=1))
    # print(ndcg_at_k([0], 5, method=1))
    # print(ndcg_at_k([1], 5, method=1))
    # print(ndcg_at_k([1, 0], 5, method=1))
    # print(ndcg_at_k([0, 1], 5, method=1))
    # print(ndcg_at_k([0, 1, 1], 5, method=1))
    # print(ndcg_at_k([0, 1, 1, 1], 5, method=1))
