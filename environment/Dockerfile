FROM python:3.13-slim@sha256:REPLACE_WITH_REAL_DIGEST
RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5
WORKDIR /app
COPY access.log /app/access.log