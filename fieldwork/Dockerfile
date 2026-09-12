FROM python:3.12-slim

WORKDIR /app
COPY fieldwork/ /app/

RUN pip install --no-cache-dir .

ENV PYTHONUNBUFFERED=1 \
    AUTOMATION_HOST=0.0.0.0 \
    PORT=8080 \
    AUTOMATION_ENABLE_GEMMA=false \
    AUTOMATION_RETENTION_MINUTES=60

EXPOSE 8080
CMD ["python", "run_web.py"]
