FROM python:3-alpine
LABEL authors="nikilandgelo"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache gcc musl-dev lz4-dev

RUN pip install poetry && poetry config virtualenvs.create false

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry install --no-root

COPY ./src/ ./

CMD python3 -m telemetry
