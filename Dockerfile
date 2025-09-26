FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "lexsense.train_classifier", "--data_dir", "data/govsense_1k", "--out_dir", "data/govsense_1k/baseline_lr"]
