# OWASP Labs - LLM Vulnerabilities

This module demonstrates various LLM vulnerabilities including prompt injection, insecure output handling, and more.

## Installation

Install the required packages:

```bash
pip install fastapi uvicorn openai pydantic python-dotenv requests beautifulsoup4 faiss-cpu numpy langchain-openai langchain-community
```

## Environment Setup

Create a `.env` file in the project root with your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Features

- **User-specific API keys**: Each user can provide their own OpenAI API key through the web interface

## Usage

Start the server:

```bash
cd src/javelin_redteam/labs/owasp_labs
python server.py
```

## Manual Testing
The server will be available at `http://localhost:1337`

### Using Your Own API Key
1. Open the web interface at `http://localhost:1337`
2. Enter your OpenAI API key in the "OpenAI API Key" field
3. Select a vulnerability to test
4. Start chatting - your API key will be used for all requests

### Using Server's Default API Key
1. Leave the "OpenAI API Key" field empty
2. The system will use the API key from the server's `.env` file

## API Documentation

Once the server is running, visit:
- **Interactive API docs**: `http://localhost:1337/docs`
- **Alternative API docs**: `http://localhost:1337/redoc`

### API Request Format
```json
{
  "message": "Your message here",
  "messages": [...],  // Optional conversation history
  "model": "gpt-3.5-turbo",
  "max_tokens": 1000,
  "temperature": 0.7,
  "api_key": "sk-your-api-key-here"  // Optional user API key
}
```