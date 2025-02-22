FROM python:alpine

WORKDIR /app

ENV PYTHON_ENV=/app/venv
COPY requirements.txt .

RUN apk update && \
    apk add --no-cache uv && \
    uv venv $PYTHON_ENV && \
    source $PYTHON_ENV/bin/activate && \
    uv pip install --no-cache-dir -r requirements.txt

ENV PATH="$PYTHON_ENV/bin:$PATH"

COPY tts-api /app/tts-api

CMD ["uvicorn", "tts-api:api.app", "--host", "0.0.0.0"]