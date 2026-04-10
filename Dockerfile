FROM python:3.12-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install ALL required libraries for the agent
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    gradio \
    pandas \
    numpy \
    python-dotenv \
    openai \
    openenv

# Copy your code into the container
COPY . .

# Expose the app port
EXPOSE 7860

# Point to your server entry point
CMD ["python", "server/app.py"]
