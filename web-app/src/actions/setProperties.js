import { api }  from '../api'
import { USER_ID_CHANGED, ALGORITHM_CHANGED, USER_ITEMS_ISSUED, USER_RECOMMENDATION_ISSUED } from "../types";

export const userIdChanged = userId => ({
   type: USER_ID_CHANGED,
   userId
});

export const algorithmChanged = algorithm => ({
    type: ALGORITHM_CHANGED,
    algorithm
});

export const userItemsIssued = userItems => ({
   type: USER_ITEMS_ISSUED,
    userItems
});

export const userRecommendarionIssued = recommendedItems => ({
    type: USER_RECOMMENDATION_ISSUED,
    recommendedItems
});

export const setUserId = (userId, algorithm) => dispatch => {
    dispatch(userIdChanged(userId));
    api.getUserItems(userId).then(userItems =>  dispatch(userItemsIssued(userItems)));
    api.getRecommendation(userId, algorithm).then(
        recommendedItems => dispatch(userRecommendarionIssued(recommendedItems)))
};
export const setAlgorithm = (userId, algorithm) => dispatch => {
    dispatch(algorithmChanged(algorithm));
    api.getRecommendation(userId, algorithm).then(
        recommendedItems => dispatch(userRecommendarionIssued(recommendedItems)));
};
