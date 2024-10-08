# Dockerfile
FROM nvidia/cuda:12.1.1-base-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    python3.10 \
    python3-pip

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]