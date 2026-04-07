FROM python:3.12-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set PYTHONPATH so 'greenhouse' is treatable as a module
ENV PYTHONPATH=/code

# Expose Gradio/FastAPI port
EXPOSE 7860

# Start the application using the module path
CMD ["python", "greenhouse/server/app.py"]
