import { USER_ID_CHANGED, ALGORITHM_CHANGED } from "../types";

export function userId(state = {}, action = {}) {
    switch (action.type) {
        case USER_ID_CHANGED:
            return action.userId;
        default:
            return state;
    }
}

export function algorithm(state = {}, action = {}) {
    switch (action.type) {
        case ALGORITHM_CHANGED:
            return action.algorithm;
        default:
            return state;
    }
}
