FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN mkdir -p /tmp/s3_data /tmp/data
RUN pip install --no-cache-dir boto3 pandas python-dotenv numpy pytest joblib boxsdk

CMD ["python", "script.py"]
