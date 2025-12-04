import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Research a company
export const researchCompany = async (companyName) => {
    const response = await api.post('/research/', { company_name: companyName });
    return response.data;
};

// Chat with RAG
export const sendChatMessage = async (companyName, prompt) => {
    const response = await api.post('/chat/', {
        company_name: companyName,
        prompt: prompt,
    });
    return response.data;
};

// Get list of companies
export const getCompanies = async () => {
    const response = await api.get('/companies/');
    return response.data;
};

// Reset company data
export const resetCompany = async (companyName) => {
    const response = await api.delete(`/reset/${companyName}`);
    return response.data;
};

// Health check
export const healthCheck = async () => {
    const response = await api.get('/health');
    return response.data;
};

export default api;
