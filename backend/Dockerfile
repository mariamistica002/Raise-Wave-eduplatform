FROM Python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/ststicfiles /app/media

EXPOSE 8000

CMD {"gunicorn", "eduplatform.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
