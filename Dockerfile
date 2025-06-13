FROM python:3.12-slim

WORKDIR /app

COPY . /app
COPY .env /app/.env


RUN pip install --no-cache-dir boto3 pandas python-dotenv numpy pytest
ENV PYTHONUNBUFFERED=1


CMD ["python", "script.py"]
