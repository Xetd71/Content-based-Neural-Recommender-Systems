import { combineReducers } from 'redux';
import { userId, algorithm } from './reducers/properties'


export default combineReducers({
    userId,
    algorithm,
});