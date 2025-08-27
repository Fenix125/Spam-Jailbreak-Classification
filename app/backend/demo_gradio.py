import gradio as gr
import uuid
import requests
from app.backend.config import settings

URL = settings.backend_adress + "/agent"
session_state = gr.State() 

def call_agent(prompt: str, history, session_id: str | None) -> str:
    """
    Sends the user's message to your FastAPI /api/agent endpoint and returns the reply.
    """
    if not session_id:
        session_id = str(uuid.uuid4())
    
    r = requests.post(URL, json={"prompt": prompt, "session_id": session_id}, timeout=120)
    r.raise_for_status()
    return r.json()["output"], session_id

demo = gr.ChatInterface(
    fn=call_agent,
    title="MyAgent",
    type="messages",
    additional_inputs=[session_state],
    additional_outputs=[session_state],
)
demo.launch(share=True)

