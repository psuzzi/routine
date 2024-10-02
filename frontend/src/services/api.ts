import axios from 'axios'

const api = axios.create({
    // environment variable to match the backend URL
    baseURL: process.env.REACT_APP_API_BASE_URL, // dev is: 'http://localhost:8080/api'
})

api.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
        // with OAuth, we will need to pass `Bearer ${token}`
        config.headers.Authorization = token // basic auth
    }
    return config
})

export default api;