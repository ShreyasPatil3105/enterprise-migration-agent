FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    python-multipart \
    streamlit \
    requests \
    docker \
    GitPython

COPY main.py app.py /app/

EXPOSE 8501

CMD ["python", "main.py"]
