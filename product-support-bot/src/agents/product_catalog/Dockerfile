FROM python:3.11-slim

# Set working directory
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src ./src
COPY data ./data

# Cloud Run will send traffic to this port
EXPOSE 8080

# Start the Product Catalog A2A server
CMD ["sh", "-c", "uvicorn src.server.product_catalog_server:app --host 0.0.0.0 --port ${PORT:-8080}"]

