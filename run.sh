#!/bin/shell
python -m venv venv
venv/Scripts/activate

export FLASK_APP=app
export FLASK_ENV=development
export SECRET_KEY=your_secret_key
export DATABASE_URI="postgresql://<your_postgres_user>:<your_postgres_password>@localhost:5432/opinion_ai"
export DATABASE_URI_TEST="postgresql://<your_postgres_user>:<your_postgres_password>@localhost:5432/opinion_ai_test"
export CACHE_TYPE=RedisCache
export CACHE_REDIS_HOST=localhost
export CACHE_REDIS_PORT=6379
export CACHE_REDIS_DB=0
export CACHE_REDIS_URL="redis://localhost:6379/opinion_ai"
export CACHE_DEFAULT_TIMEOUT=500
export UPLOAD_DIR="/var/deep-opinion/upload"

pip install -r requirements.txt
flask run -h 0.0.0.0 -p 5000
