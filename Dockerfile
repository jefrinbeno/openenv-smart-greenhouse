FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Install dependencies
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

COPY . .

# We no longer need chmod on a non-existent server/app.py
# Instead, we run the app directly via uvicorn from the new package
CMD ["uvicorn", "greenhouse_package.env_server:app", "--host", "0.0.0.0", "--port", "7860"]
