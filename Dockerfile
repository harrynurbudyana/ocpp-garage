FROM python:3.11.3-slim-bullseye

RUN apt-get update && apt-get install -y build-essential curl git wkhtmltopdf
RUN curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | tee /usr/share/keyrings/stripe.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | tee -a /etc/apt/sources.list.d/stripe.list && \
    apt update && \
    apt install stripe


RUN mkdir -p /usr/src/csms/backend
RUN mkdir -p /usr/src/csms/frontend
RUN mkdir -p /tmp/static

WORKDIR /usr/src/csms

COPY frontend /usr/src/csms/frontend
COPY backend /usr/src/csms/backend

ENV PYTHONPATH=/usr/src/csms/backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=$GITHUB_TOKEN


RUN pip install --no-cache git+https://heroyooki:${GITHUB_TOKEN}@github.com/heroyooki/pyocpp_contrib.git
RUN pip install -r backend/requirements.txt --upgrade pip
