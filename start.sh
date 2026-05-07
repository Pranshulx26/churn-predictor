#!/bin/bash

# Start FastAPI in background
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Wait until FastAPI is actually ready, not just started
echo "Waiting for FastAPI to start..."
while ! curl -s http://127.0.0.1:8000/health > /dev/null; do
    sleep 1
done
echo "FastAPI is ready."

# Now start Streamlit
streamlit run src/frontend/app.py --server.port 8501 --server.address 0.0.0.0