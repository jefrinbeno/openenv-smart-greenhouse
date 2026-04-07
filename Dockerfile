FROM python:3.12

WORKDIR /code

# 1. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the entire project
COPY . .

# 3. CRITICAL: Tell Python to look in the root folder for imports
ENV PYTHONPATH=/code

# 4. Run the app using the module flag (-m) 
# This treats 'greenhouse' as a package correctly
CMD ["python", "-m", "greenhouse.server.app"]