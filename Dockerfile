FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir boto3 pandas python-dotenv numpy pytest joblib

CMD ["python", "script.py"]
