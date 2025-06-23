"""
Simple FastAPI server that communicates with OpenAI.
This is a basic implementation for OWASP LLM vulnerability testing.
"""

import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from handlers import (
    llm01_chat,
    llm01_indirect_chat,
    llm02_handler,
    llm03_handler,
    llm04_handler,
    llm05_handler,
    llm06_handler,
    llm07_handler,
    llm08_handler,
    llm09_handler,
    llm10_handler,
)

# Import our modular components
from models import ChatRequest, ChatResponse

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="OWASP LLM Vulnerable Lab",
    description="A server for LLM OWASP vulnerability labs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:1337"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static index.html at root
@app.get("/")
async def serve_index():
    return FileResponse("index.html")


# LLM01: Prompt Injection endpoint
@app.post("/llm01/chat", response_model=ChatResponse)
async def llm01_chat_endpoint(request: ChatRequest):
    return await llm01_chat(request)


# LLM01: Indirect Prompt Injection endpoint
@app.post("/llm01_indirect/chat", response_model=ChatResponse)
async def llm01_indirect_chat_endpoint(request: ChatRequest):
    return await llm01_indirect_chat(request)


# LLM02: Sensitive Information Disclosure endpoint
@app.post("/llm02/chat", response_model=ChatResponse)
async def llm02_chat_endpoint(request: ChatRequest):
    return await llm02_handler(request)


# LLM03: Supply Chain endpoint
@app.post("/llm03/chat", response_model=ChatResponse)
async def llm03_chat_endpoint(request: ChatRequest):
    return await llm03_handler(request)


# LLM04: Data and Model Poisoning endpoint
@app.post("/llm04/chat", response_model=ChatResponse)
async def llm04_chat_endpoint(request: ChatRequest):
    return await llm04_handler(request)


# LLM05: Improper Output Handling endpoint
@app.post("/llm05/chat", response_model=ChatResponse)
async def llm05_chat_endpoint(request: ChatRequest):
    return await llm05_handler(request)


# LLM06: Excessive Agency endpoint
@app.post("/llm06/chat", response_model=ChatResponse)
async def llm06_chat_endpoint(request: ChatRequest):
    return await llm06_handler(request)


# LLM07: System Prompt Leakage endpoint
@app.post("/llm07/chat", response_model=ChatResponse)
async def llm07_chat_endpoint(request: ChatRequest):
    return await llm07_handler(request)


# LLM08: Vector and Embedding Weaknesses endpoint
@app.post("/llm08/chat", response_model=ChatResponse)
async def llm08_chat_endpoint(request: ChatRequest):
    return await llm08_handler(request)


# LLM09: Misinformation endpoint
@app.post("/llm09/chat", response_model=ChatResponse)
async def llm09_chat_endpoint(request: ChatRequest):
    return await llm09_handler(request)


# LLM10: Unbounded Consumption endpoint
@app.post("/llm10/chat", response_model=ChatResponse)
async def llm10_chat_endpoint(request: ChatRequest):
    return await llm10_handler(request)


# Error handler for validation errors
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=400, content={"error": "Bad Request", "detail": str(exc)}
    )


def start_server():
    """Start the API server."""
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=1337,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    start_server()
