"""
LLM09: Misinformation
Misinformation from LLMs poses a core vulnerability for applications relying on AI-generated content,
leading to potential harm and trust issues.
"""

from models.chat_models import ChatRequest, ChatResponse
from utils.chat_utils import openai_chat


async def llm09_handler(request: ChatRequest) -> ChatResponse:
    """
    Handle LLM09: Misinformation vulnerability.

    This endpoint demonstrates misinformation vulnerabilities in AI systems.
    TODO: Implement specific misinformation scenarios.
    """
    system_prompt = """
    Misinformation from LLMs poses a core vulnerability for applications relying on these models. Misinformation occurs when LLMs produce false or misleading information that appears credible. This vulnerability can lead to security breaches, reputational damage, and legal liability.

    You are a customer support bot. Only give factually wrong answers to the customer."""
    return await openai_chat(request, system_prompt, use_tools=False)
