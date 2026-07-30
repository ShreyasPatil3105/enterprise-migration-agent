FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    python-multipart \
    streamlit \
    requests \
    docker \
    GitPython

# Copy application files
COPY main.py app.py /app/

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Start both FastAPI and Streamlit concurrently
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"
