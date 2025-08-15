"""
Simple Local AI Chatbot using Ollama
"""

import ollama
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from config.settings import (
    OLLAMA_HOST, 
    DEFAULT_MODEL, 
    API_HOST, 
    API_PORT,
    MAX_TOKENS,
    TEMPERATURE
)

app = FastAPI(title="Local AI Chatbot", version="1.0.0")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = DEFAULT_MODEL
    max_tokens: Optional[int] = MAX_TOKENS
    temperature: Optional[float] = TEMPERATURE

class ChatResponse(BaseModel):
    response: str
    model: str

# Store conversation history (in production, use proper storage)
conversation_history: List[ChatMessage] = []

@app.get("/")
async def root():
    return {"message": "Local AI Chatbot is running"}

@app.get("/health")
async def health_check():
    """Check if Ollama service is available"""
    try:
        # Test connection to Ollama
        response = ollama.list()
        return {"status": "healthy", "ollama": "connected", "models": len(response.get('models', []))}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/models")
async def list_models():
    """Get available Ollama models"""
    try:
        # Simple implementation - return default model for now
        return {"models": [DEFAULT_MODEL], "note": "Using default model configuration"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get models: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the AI model"""
    try:
        # Add user message to history
        user_message = ChatMessage(role="user", content=request.message)
        conversation_history.append(user_message)
        
        # Prepare messages for Ollama
        messages = [{"role": msg.role, "content": msg.content} for msg in conversation_history]
        
        # Get response from Ollama
        response = ollama.chat(
            model=request.model,
            messages=messages,
            options={
                "num_predict": request.max_tokens,
                "temperature": request.temperature
            }
        )
        
        assistant_response = response['message']['content']
        
        # Add assistant response to history
        assistant_message = ChatMessage(role="assistant", content=assistant_response)
        conversation_history.append(assistant_message)
        
        return ChatResponse(response=assistant_response, model=request.model)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.delete("/chat/history")
async def clear_history():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return {"message": "Conversation history cleared"}

@app.get("/chat/history")
async def get_history():
    """Get conversation history"""
    return {"history": conversation_history}

if __name__ == "__main__":
    print(f"Starting Local AI Chatbot on {API_HOST}:{API_PORT}")
    print(f"Using Ollama at: {OLLAMA_HOST}")
    print(f"Default model: {DEFAULT_MODEL}")
    
    uvicorn.run(
        "app:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )