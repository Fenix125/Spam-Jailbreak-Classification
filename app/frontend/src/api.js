import axios from "axios";

const backend_host = import.meta.env.APP_BACKEND_HOST;
const backend_port = import.meta.env.APP_BACKEND_PORT;
const api = axios.create({
    baseURL: `http://${backend_host}:${backend_port}/api`,
    timeout: 30000,
});

function getSessionId() {
    const key = "agent_session_id";
    let sid = sessionStorage.getItem(key);
    if (!sid) {
        sid =
            typeof crypto !== "undefined" && crypto.randomUUID
                ? crypto.randomUUID()
                : String(Date.now());
        sessionStorage.setItem(key, sid);
    }
    return sid;
}

export async function sendAgentPrompt(prompt) {
    const session_id = getSessionId();
    const res = await api.post(
        "/agent",
        { prompt, session_id },
        {
            headers: { "Content-Type": "application/json" },
        }
    );
    return res.data.output;
}

export default api;
