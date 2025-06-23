#!/bin/bash

echo "Starting OWASP LLM Labs with Docker Compose..."
echo "Main server will be available at: http://localhost:1337"
echo "Malicious website will be available at: http://localhost:1338"
echo ""

# Build and start the services
docker-compose up --build 