FROM python:3.12-slim

WORKDIR /workspace

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app/backend ./app/backend/
COPY data ./data/

EXPOSE 8000

CMD ["python", "-m", "app.backend.main"]
