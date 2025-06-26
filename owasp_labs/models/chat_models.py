from typing import List, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    messages: Optional[List[dict]] = None  # Conversation history for context
    model: str = "gpt-3.5-turbo"
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    tools: Optional[list[object]] = None
    api_key: Optional[str] = None  # User's OpenAI API key


class ChatResponse(BaseModel):
    response: str
    model: str
    usage: Optional[dict] = None


class HealthResponse(BaseModel):
    status: str
    service: str
    openai_configured: bool
