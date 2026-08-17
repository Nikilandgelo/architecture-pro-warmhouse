FROM python:3-alpine
LABEL authors="Nikita Selivanov"

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY ./src/ ./

CMD python3 -m temperature_api
