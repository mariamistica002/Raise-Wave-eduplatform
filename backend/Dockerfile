FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create media & static dirs
RUN mkdir -p media staticfiles

EXPOSE 8000

CMD ["gunicorn", "eduplatform.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
