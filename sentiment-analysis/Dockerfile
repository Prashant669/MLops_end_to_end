## Stage1 -builder

FROM python:3.10-slim AS builder
WORKDIR /build
COPY requirements-app.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements-app.txt

### Stage 2 - runtime

FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl \
      && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /install /usr/local

COPY app.py .
COPY src/ ./src/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh && mkdir -p models

RUN useradd --no-create-home --shell /bin/false appuser \
      && chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1
EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]