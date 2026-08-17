FROM python:3-alpine
LABEL authors="nikilandgelo"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry install --no-root

COPY ./src/ ./

CMD python3 -m automation_engine
