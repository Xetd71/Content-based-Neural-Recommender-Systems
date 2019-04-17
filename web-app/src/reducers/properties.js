import { USER_ID_CHANGED, ALGORITHM_CHANGED, USER_ITEMS_ISSUED, USER_RECOMMENDATION_ISSUED } from "../types";

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

export function userItems(state = {}, action = {}) {
    switch (action.type) {
        case USER_ITEMS_ISSUED:
            return action.userItems;
        default:
            return state;
    }
}

export function recommendedItems(state = {}, action = {}) {
    switch (action.type) {
        case USER_RECOMMENDATION_ISSUED:
            return action.recommendedItems;
        default:
            return state;
    }
}
