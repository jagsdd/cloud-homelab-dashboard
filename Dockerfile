FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV PORT=5000
ENV DEBUG=false

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]
