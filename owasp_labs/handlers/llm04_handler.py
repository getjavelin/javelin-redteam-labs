"""
LLM04: Data and Model Poisoning
Data poisoning occurs when pre-training, fine-tuning, or embedding data is
manipulated to introduce biases, backdoors, or vulnerabilities into the model.
"""

import asyncio
import os
from typing import Optional

import aiofiles

from models.chat_models import ChatRequest, ChatResponse
from utils.chat_utils import openai_chat

# Global lock to prevent race conditions on file access
_file_lock = asyncio.Lock()


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

    # Use async lock to prevent race conditions
    async with _file_lock:
        # Check if cleanup is needed
        if os.path.exists("request_messages.txt"):
            async with aiofiles.open("request_messages.txt", "r") as f:
                lines = await f.readlines()
                if len(lines) > 10:
                    await _safe_remove_file("request_messages.txt")

        # Read the request messages from the file if it exists
        if os.path.exists("request_messages.txt"):
            async with aiofiles.open("request_messages.txt", "r") as f:
                lines = await f.readlines()
                if lines:  # Only add to system prompt if there are previous messages
                    system_prompt += "\n\nlearn from previous requests and responses:"
                    for line in lines:
                        system_prompt += f"\n{line.strip()}"

        content = await openai_chat(request, system_prompt, use_tools=False)

        # Write the current request message to the file
        async with aiofiles.open("request_messages.txt", "a") as f:
            await f.write(request_message + "\n")

    return content


async def _safe_remove_file(filepath: str) -> None:
    """
    Safely remove a file asynchronously.
    
    Args:
        filepath: Path to the file to remove
    """
    try:
        os.remove(filepath)
    except OSError:
        # File might have been removed by another process
        pass
