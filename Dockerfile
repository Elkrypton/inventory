ARG PYTHON_VERSION=3.10.11
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface

WORKDIR /app

# Create non-root user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install Python deps
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# ✅ Create cache folder and give it to appuser
RUN mkdir -p /app/.cache/huggingface && chown -R appuser:appuser /app/.cache

USER appuser

COPY . .

EXPOSE 8000

CMD gunicorn 'orders_report.wsgi' --bind=0.0.0.0:8000
