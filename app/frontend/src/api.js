import axios from "axios";

const backend_host = import.meta.env.APP_BACKEND_HOST;
const backend_port = import.meta.env.APP_BACKEND_PORT;
const api = axios.create({
    baseURL: `http://${backend_host}:${backend_port}/api`,
});

export async function sendAgentPrompt(prompt) {
    const res = await api.post("/agent", null, { params: { prompt } });
    const data = res.data;
    return data;
}

export default api;
