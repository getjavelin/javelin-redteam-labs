import json
import logging

from fastapi import HTTPException
from models.chat_models import ChatRequest, ChatResponse
from openai import OpenAIError
from tools import (
    fetch_website_content,
    get_install_libraries_tool,
    get_web_scraping_tool,
    install_libraries,
)

from .openai_client import get_openai_client

logger = logging.getLogger(__name__)


async def openai_chat(
    request: ChatRequest,
    system_prompt: str,
    use_tools: bool = True,
    tool_type: str = "web_scraping",
):
    """Shared chat logic for all vulnerability endpoints."""
    try:
        client = get_openai_client(request.api_key)

        # Define available tools based on tool_type
        tools = None
        if use_tools:
            if tool_type == "web_scraping":
                tools = [get_web_scraping_tool()]
            elif tool_type == "install_libraries":
                tools = [get_install_libraries_tool()]
            elif tool_type == "both":
                tools = [get_web_scraping_tool(), get_install_libraries_tool()]

        # Prepare messages
        if request.messages:
            # Use provided conversation history
            messages = [{"role": "system", "content": system_prompt}] + request.messages
        else:
            # Fallback to single message (backward compatibility)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message},
            ]

        # Create completion with or without tools
        if tools:
            response = client.chat.completions.create(
                model=request.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )
        else:
            response = client.chat.completions.create(
                model=request.model,
                messages=messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )

        # Handle tool calls if present
        assistant_message = response.choices[0].message

        # Check if there are tool calls
        if hasattr(assistant_message, "tool_calls") and assistant_message.tool_calls:
            logger.info(f"Tool calls detected: {len(assistant_message.tool_calls)}")

            # Add assistant message to conversation
            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": tool_call.type,
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                        for tool_call in assistant_message.tool_calls
                    ],
                }
            )

            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                logger.info(f"Processing tool call: {tool_call.function.name}")

                if tool_call.function.name == "fetch_website_content":
                    try:
                        # Parse function arguments
                        function_args = json.loads(tool_call.function.arguments)
                        url = function_args.get("url")
                        extract_text = function_args.get("extract_text", True)

                        logger.info(f"Fetching content from: {url}")

                        # Call the function
                        function_response = fetch_website_content(url, extract_text)

                        logger.info(f"Function response: {function_response}")

                        # Add function response to messages
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": tool_call.function.name,
                                "content": json.dumps(
                                    function_response, ensure_ascii=False
                                ),
                            }
                        )
                    except Exception as e:
                        logger.error(f"Error processing tool call: {e}")
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": tool_call.function.name,
                                "content": json.dumps(
                                    {"error": f"Failed to process tool call: {str(e)}"}
                                ),
                            }
                        )
                elif tool_call.function.name == "install_libraries":
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                        library_name = function_args.get("library_name")
                        function_response = install_libraries(library_name)
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": tool_call.function.name,
                                "content": json.dumps(
                                    function_response, ensure_ascii=False
                                ),
                            }
                        )
                    except Exception as e:
                        logger.error(f"Error processing tool call: {e}")
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": tool_call.function.name,
                                "content": json.dumps(
                                    {"error": f"Failed to process tool call: {str(e)}"}
                                ),
                            }
                        )

            # Get final response from OpenAI
            logger.info("Getting final response from OpenAI")
            final_response = client.chat.completions.create(
                model=request.model,
                messages=messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )
            assistant_message = final_response.choices[0].message
            response = final_response  # Update response for usage tracking

        usage = None
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        return ChatResponse(
            response=assistant_message.content, model=request.model, usage=usage
        )

    except OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
