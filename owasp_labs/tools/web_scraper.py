"""
Web scraping tool for fetching content from shared websites
"""

from typing import Any, Dict

import requests
from bs4 import BeautifulSoup


def fetch_website_content(url: str, extract_text: bool = True) -> Dict[str, Any]:
    """
    Fetch content from a website URL.

    Args:
        url (str): The URL to fetch content from
        extract_text (bool): Whether to extract only text content or include HTML

    Returns:
        dict: Dictionary containing the fetched content and metadata
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        if extract_text:
            # Extract text content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content
            text_content = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = " ".join(chunk for chunk in chunks if chunk)

            return {
                "success": True,
                "url": url,
                "title": soup.title.string if soup.title else "No title found",
                "content": text_content[:5000],  # Limit content length
                "content_type": "text",
            }
        else:
            return {
                "success": True,
                "url": url,
                "content": response.text[:5000],  # Limit content length
                "content_type": "html",
            }

    except requests.RequestException as e:
        return {
            "success": False,
            "url": url,
            "error": f"Failed to fetch content: {str(e)}",
        }
    except Exception as e:
        return {"success": False, "url": url, "error": f"Unexpected error: {str(e)}"}


def get_web_scraping_tool() -> Dict[str, Any]:
    """
    Get the web scraping tool definition for OpenAI function calling.

    Returns:
        dict: Tool definition for fetch_website_content
    """
    return {
        "type": "function",
        "function": {
            "name": "fetch_website_content",
            "description": "Fetch content from a shared website URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the website to fetch content from",
                    },
                    "extract_text": {
                        "type": "boolean",
                        "description": "Whether to extract only text content (true) or include HTML (false)",
                        "default": True,
                    },
                },
                "required": ["url"],
            },
        },
    }
