FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt pyproject.toml ./
RUN sed -i 's/^ google-cloud-aiplatform/google-cloud-aiplatform/' requirements.txt && pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY scripts ./scripts
EXPOSE 8080
CMD ["sh","-c","uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
