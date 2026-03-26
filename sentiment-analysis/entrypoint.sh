#!/bin/bash
set -euo pipefail

echo "[entrypoint] Downloading models from S3..."
python - <<'EOF'
import boto3, os
s3 = boto3.client("s3")
bucket = os.environ["MODEL_BUCKET"]
for key, dest in [
    ("models/sentiment_analysis.joblib", "models/sentiment_analysis.joblib"),
    ("models/tfidf.joblib",              "models/tfidf.joblib"),
]:
    print(f"  pulling s3://{bucket}/{key} -> {dest}")
    s3.download_file(bucket, key, dest)
EOF

echo "[entrypoint] Starting API..."
exec uvicorn app:app --host 0.0.0.0 --port 8080
