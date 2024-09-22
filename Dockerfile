FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry==1.5.1

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 5000

CMD ["flask", "--app=app", "run", "--host=0.0.0.0"]
