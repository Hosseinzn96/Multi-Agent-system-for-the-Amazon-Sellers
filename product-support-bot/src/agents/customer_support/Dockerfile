FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data

EXPOSE 8080

# Start the Customer Support A2A server
CMD ["sh", "-c", "uvicorn src.server.customer_support_server:app --host 0.0.0.0 --port ${PORT:-8080}"]
