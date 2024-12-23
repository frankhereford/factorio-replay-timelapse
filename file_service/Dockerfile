FROM python:3.9-slim

WORKDIR /app

# Install necessary packages including fonts
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu-core gunicorn \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run", "--reload"]
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "6", "--threads", "4", "app:app"]