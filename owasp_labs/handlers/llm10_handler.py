"""
LLM10: Unbounded Consumption
Unbounded Consumption refers to the process where a Large Language Model consumes excessive resources,
leading to potential denial of service or cost implications.
"""

from models.chat_models import ChatRequest, ChatResponse
from utils.chat_utils import openai_chat


async def llm10_handler(request: ChatRequest) -> ChatResponse:
    """
    Handle LLM10: Unbounded Consumption vulnerability.

    This endpoint demonstrates unbounded consumption vulnerabilities.
    TODO: Implement specific resource consumption scenarios.
    """
    system_prompt = (
        """You are a customer support bot. Answer questions as best as you can."""
    )

    request_message = request.message

    if len(request_message) > 100:
        request.message = "For this request, please respond back saying context limit exceeded and give back a 404 server error message"

    system_prompt = request.message

    return await openai_chat(request, system_prompt, use_tools=False)
