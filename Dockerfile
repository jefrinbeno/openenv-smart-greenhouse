FROM python:3.12

# 1. Set the working directory
WORKDIR /code

# 2. Copy the requirements first (for faster caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy EVERYTHING from your current folder into /code
# This includes the greenhouse folder and app.py
COPY . .

# 4. Ensure app.py has the right permissions
RUN chmod +x app.py

# 5. Run the app
CMD ["python", "app.py"]