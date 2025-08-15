#!/bin/bash

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
until curl -f http://localhost:11434/api/tags >/dev/null 2>&1; do
    echo "Ollama not ready yet, waiting..."
    sleep 5
done

echo "Ollama is ready! Pulling llama3.2:1b model..."

# Pull the model if it doesn't exist
if ! ollama list | grep -q "llama3.2:1b"; then
    echo "Pulling llama3.2:1b model..."
    ollama pull llama3.2:1b
else
    echo "Model llama3.2:1b already exists."
fi

echo "Model initialization complete!"