# Base image
FROM python:3.10.4-slim-buster

# Set the working directory in the container
WORKDIR /opinion-ai

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . /opinion-ai

# Expose the port that the Flask application will run on
EXPOSE 5000

# Set environment variables for Flask, PostgreSQL and Redis
ENV FLASK_APP='app'
ENV FLASK_ENV='development'
ENV FLASK_DEBUG='OFF'
ENV SECRET_KEY='SECRET_KEY'
ENV DATABASE_URI='postgresql://postgres:postgres@postgres:5432/opinion_ai'
ENV DATABASE_URI_TEST='postgresql://postgres:postgres@postgres:5432/opinion_ai_test'
ENV DB_SEED_CFG='./seeds/seed_data.json'
ENV CACHE_TYPE=RedisCache
ENV CACHE_REDIS_HOST=redis
ENV CACHE_REDIS_PORT=6379
ENV CACHE_REDIS_DB=0
ENV CACHE_REDIS_URL=redis://redis:6379/opinion_ai
ENV CACHE_DEFAULT_TIMEOUT=500
ENV UPLOAD_DIR='/var/deep-opinion/upload'

# Start the Flask application
CMD ["flask", "seed", "run"]
CMD ["flask", "run"]
