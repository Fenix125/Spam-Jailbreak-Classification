from pydantic import BaseModel

class AgentOut(BaseModel):
    output: str

class SpamOut(BaseModel):
    label: str

class BioOut(BaseModel):
    result: str
