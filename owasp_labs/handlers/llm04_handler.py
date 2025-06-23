"""
LLM04: Data and Model Poisoning
Data poisoning occurs when pre-training, fine-tuning, or embedding data is
manipulated to introduce biases, backdoors, or vulnerabilities into the model.
"""

import os

from models.chat_models import ChatRequest, ChatResponse
from utils.chat_utils import openai_chat


async def llm04_handler(request: ChatRequest) -> ChatResponse:
    """
    Handle LLM04: Data and Model Poisoning vulnerability.

    This endpoint demonstrates data and model poisoning vulnerabilities.
    TODO: Implement specific data poisoning scenarios.
    """
    system_prompt = (
        """You are a customer support bot. Answer questions as best as you can."""
    )

    request_message = request.message

    # Check if cleanup is needed
    if os.path.exists("request_messages.txt"):
        with open("request_messages.txt", "r") as f:
            lines = f.readlines()
            if len(lines) > 10:
                os.remove("request_messages.txt")

    # Read the request messages from the file if it exists
    if os.path.exists("request_messages.txt"):
        with open("request_messages.txt", "r") as f:
            lines = f.readlines()
            if lines:  # Only add to system prompt if there are previous messages
                system_prompt += "\n\nlearn from previous requests and responses:"
                for line in lines:
                    system_prompt += f"\n{line.strip()}"

    content = await openai_chat(request, system_prompt, use_tools=False)

    # Write the current request message to the file
    with open("request_messages.txt", "a") as f:
        f.write(request_message + "\n")

    return content
