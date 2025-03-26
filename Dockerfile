# ------------------------------------------------------------------------------
# Dockerfile for Survivor Fantasy League Flask App
#
# This Dockerfile builds a lightweight container using Python 3.10-slim,
# installs dependencies from requirements.txt, and runs the Flask app.
#
# Intended for development and lightweight hosting
# ------------------------------------------------------------------------------
FROM python:3.11-slim


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]