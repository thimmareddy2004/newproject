FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
COPY ../shared ./shared

EXPOSE 5002

CMD ["python", "app.py"]