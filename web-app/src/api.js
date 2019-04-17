import axios from 'axios';

const api =  {
    getUserItems: (userId) => axios.get(`user_items/${userId}`).then(res => res.data),
    getRecommendation: (userId, algorithm) => axios.get(`${algorithm}/${userId}`).then(res => res.data),
};

export {
    api,
}

