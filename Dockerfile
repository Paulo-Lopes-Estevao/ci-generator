FROM python:3.11.4-slim as compile-image

WORKDIR /app

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN pip install -U .

FROM python:3.11.4-alpine as run-test-stage

RUN pytest ./..

FROM python:3.11.4-alpine as build-stage

WORKDIR /app

COPY --from=compile-image /opt/venv /opt/venv

EXPOSE 8000

ENV PATH="/opt/venv/bin:$PATH"

CMD ["tail", "-f", "/dev/null"]
