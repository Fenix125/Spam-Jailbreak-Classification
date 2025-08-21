import axios from "axios";

const baseUrl = import.meta.env.APP_BASE_URL;
const api = axios.create({
    baseURL: baseUrl,
});

export async function sendAgentPrompt(prompt) {
    const res = await api.post("/agent", null, { params: { prompt } });
    const data = res.data;
    return data;
}

export default api;
