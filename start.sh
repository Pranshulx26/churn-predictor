#!/bin/bash

# Start FastAPI internally
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

echo "Waiting for FastAPI..."
while ! curl -s http://127.0.0.1:8000/health > /dev/null; do
    sleep 1
done

echo "FastAPI is ready."

# Start Streamlit on Render's assigned port
streamlit run src/frontend/app.py \
    --server.port $PORT \
    --server.address 0.0.0.0