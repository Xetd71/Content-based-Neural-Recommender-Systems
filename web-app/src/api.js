import axios from 'axios';

const api =  {
    getUserItems: (userId) => axios.get(`user_items/${userId}`).then(res => res.data),
    getALSRecommendation: (userId) => axios.get(`user_items/${userId}`).then(res => res.data),
};

export {
    api,
}

