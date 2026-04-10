FROM python:3.12-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install ALL mandatory and helper libraries
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

# Copy the entire project
COPY . .

# Ensure server/app.py is executable
RUN chmod +x server/app.py

# Expose the mandatory port for the validator
EXPOSE 7860

# The command MUST point to the root-level server/app.py
CMD ["python", "server/app.py"]
