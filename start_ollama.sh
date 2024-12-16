#!/bin/bash
echo "Running OLLAMA server"
ollama serve &
sleep 5
ollama run mistral-nemo &
