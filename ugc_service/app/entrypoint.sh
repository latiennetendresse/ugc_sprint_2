#!/bin/sh

echo "Waiting for KAFKA..."

while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
  sleep 5
  echo "KAFKA is not started"
done

echo "😗 KAFKA started"


gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app

exec "$@"
