import { combineReducers } from 'redux';
import { userId, algorithm, userItems, recommendedItems } from './reducers/properties'


export default combineReducers({
    userId,
    algorithm,
    userItems,
    recommendedItems,
});