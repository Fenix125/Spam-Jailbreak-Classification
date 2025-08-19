from langchain_openai import ChatOpenAI

def build_llm(model: str, api_key: str, temperature = 0.2):
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key,
    )
