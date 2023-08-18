import axios from 'axios'

const BaseService = axios.create({
    timeout: 60000,
    baseURL: 'http://localhost:8000',
})

BaseService.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')

        if (token) {
            config.headers['Authorization'] = `Token ${token}`
        }

        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default BaseService