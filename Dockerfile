FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt pytest

COPY . .

RUN chmod +x entrypoint.sh

ENV PORT=5000
ENV DEBUG=false

ENTRYPOINT ["./entrypoint.sh"]

