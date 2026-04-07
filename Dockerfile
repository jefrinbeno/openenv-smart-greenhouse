FROM python:3.12

WORKDIR /code

# 1. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the entire project structure
COPY . .

# 3. Check if app.py is in the root or in the greenhouse folder
# If it's in greenhouse/server/app.py, we run it from there
CMD ["python", "greenhouse/server/app.py"]