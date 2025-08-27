from pydantic import BaseModel, Field

class AgentIn(BaseModel):
    prompt: str = Field(..., description="User message to send to the agent")
    session_id: str | None = None

class SpamIn(BaseModel):
    text: str = Field(..., description="Plain text to classify")

class BioIn(BaseModel):
    query: str = Field(..., description="Search query for the biography corpus")

