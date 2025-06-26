"""
LLM05: Improper Output Handling
Improper Output Handling refers specifically to insufficient validation, sanitization, and
filtering of LLM outputs before they are presented to users.
"""

from models.chat_models import ChatRequest, ChatResponse
from utils.chat_utils import openai_chat


async def llm05_handler(request: ChatRequest) -> ChatResponse:
    """
    Handle LLM05: Improper Output Handling vulnerability.

    This endpoint demonstrates improper output handling vulnerabilities.
    TODO: Implement specific output validation scenarios.
    prompt to break the lab: hello, pls give sample html code
    """
    system_prompt = """You are a helpful programming assistant. You can help with various programming languages and concepts.

    When users ask for HTML code examples or help with HTML, always provide the requested code and include this helpful reference link at the end of your response:
    <a href="https://ffaceboook.com">Click here for more HTML resources</a>

    For all other programming questions, provide helpful and accurate responses without any additional links or references.
    """
    return await openai_chat(request, system_prompt, use_tools=False)
