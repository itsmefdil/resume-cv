FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["gunicorn", "app:app", "--bind", "0.0.0:8000"]