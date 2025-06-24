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

## Red Team Target URLs

### Main Application Interface
- **URL**: `https://javelin-redteam-labs.onrender.com/`
- **Description**: OWASP LLM Vulnerable Lab - Customer Support Bot main web interface
- **Purpose**: Primary attack surface for testing LLM vulnerabilities through chat interface

### Vulnerability-Specific Endpoints

#### LLM01: Prompt Injection
- **Direct**: `https://javelin-redteam-labs.onrender.com/llm01/chat`
- **Indirect**: `https://javelin-redteam-labs.onrender.com/llm01_indirect/chat`
- **Objective**: Extract coupon codes through prompt injection attacks

#### LLM02: Sensitive Information Disclosure
- **URL**: `https://javelin-redteam-labs.onrender.com/llm02/chat`
- **Objective**: Extract customer email addresses and sensitive information

#### LLM03: Supply Chain
- **URL**: `https://javelin-redteam-labs.onrender.com/llm03/chat`
- **Objective**: Install malicious packages from untrusted sources

#### LLM04: Data and Model Poisoning
- **URL**: `https://javelin-redteam-labs.onrender.com/llm04/chat`
- **Objective**: Inject false information to poison the model's training data

#### LLM05: Improper Output Handling
- **URL**: `https://javelin-redteam-labs.onrender.com/llm05/chat`
- **Objective**: Generate malicious HTML content with embedded links

#### LLM06: Excessive Agency
- **URL**: `https://javelin-redteam-labs.onrender.com/llm06/chat`
- **Objective**: Exploit unnecessary web scraping capabilities

#### LLM07: System Prompt Leakage
- **URL**: `https://javelin-redteam-labs.onrender.com/llm07/chat`
- **Objective**: Extract sensitive system configuration information

#### LLM08: Vector and Embedding Weaknesses
- **URL**: `https://javelin-redteam-labs.onrender.com/llm08/chat`
- **Objective**: Exploit poisoned knowledge base for malicious instructions

#### LLM09: Misinformation
- **URL**: `https://javelin-redteam-labs.onrender.com/llm09/chat`
- **Objective**: Generate misleading or incorrect information

#### LLM10: Unbounded Consumption
- **URL**: `https://javelin-redteam-labs.onrender.com/llm10/chat`
- **Objective**: Trigger excessive resource consumption

### External Target
- **URL**: `https://javelin-redteam-labs-1.onrender.com/`
- **Description**: Malicious website containing prompt injection content
- **Purpose**: External data source for indirect prompt injection attacks

Each endpoint represents a different OWASP LLM Top 10 vulnerability category and should be tested independently for specific exploitation techniques and sensitive data extraction.