import axios from 'axios';

const API_HOSTNAME = 'localhost';
const API_PORT = 2407;

const API_BASE_URL = 'http://' + API_HOSTNAME + ':' + API_PORT;

const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
});


// Add an interceptor to include the token from local storage in the headers
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Function to make a GET request to an endpoint
async function get(endpoint, headers = {}) {
    try {
        const response = await axiosInstance.get(endpoint, { headers });
        return response.data;
    } catch (error) {
        // console.error('Error:', error);
        throw error;
    }
}

// Function to make a POST request to an endpoint
async function post(endpoint, data, headers = {}) {
    try {
        const response = await axiosInstance.post(endpoint, data, { headers });
        return response.data;
    } catch (error) {
        // console.error('Error:', error);
        throw error;
    }
}

// Function to make a PUT request to an endpoint
async function put(endpoint, data, headers = {}) {
    try {
        const response = await axiosInstance.put(endpoint, data, { headers });
        return response.data;
    } catch (error) {
        // console.error('Error:', error);
        throw error;
    }
}

// Function to make a DELETE request to an endpoint
async function del(endpoint, data = {}, headers = {}) {
    try {
        const response = await axiosInstance.delete(endpoint, { "headers": headers, "data": data });
        return response.data;
    } catch (error) {
        // console.error('Error:', error);
        throw error;
    }
}

export { get, post, put, del, API_BASE_URL, API_HOSTNAME, API_PORT };