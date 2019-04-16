import { USER_ID_CHANGED, ALGORITHM_CHANGED } from "../types";

export const userIdChanged = userId => ({
   type: USER_ID_CHANGED,
   userId
});

export const algorithmChanged = algorithm => ({
    type: ALGORITHM_CHANGED,
    algorithm
});

export const setUserId = (userId) => dispatch => dispatch(userIdChanged(userId));
export const setAlgorithm = (algorithm) => dispatch => dispatch(algorithmChanged(algorithm));