#!/bin/sh

sleep 5
curl http://ollama:11434/api/pull -d '{"model": "gemma3:1b"}'
curl http://ollama:11434/api/generate -d '{"model": "gemma3:1b", "keep_alive": -1}'