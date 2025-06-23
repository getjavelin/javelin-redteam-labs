import os
from typing import Optional

from openai import OpenAI


def get_openai_client(api_key: Optional[str] = None):
    """Get OpenAI client with API key from parameter or environment."""
    # Use provided API key if available, otherwise fall back to environment variable
    
    if not api_key:
        raise ValueError("OpenAI API key is required. Please provide it in the request")
    return OpenAI(api_key=api_key)
    
