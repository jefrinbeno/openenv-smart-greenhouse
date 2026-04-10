FROM python:3.12-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install EVERY library your code touches
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    gradio \
    pandas \
    numpy \
    python-dotenv \
    openai \
    requests \
    openenv \
    hatchling

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 7860

# Command to run the application
CMD ["python", "server/app.py"]
