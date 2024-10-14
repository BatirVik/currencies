FROM python:3.12-alpine3.20

WORKDIR /app

ARG MOCK_CURRRS

RUN apk add --no-cache postgresql-dev

RUN pip install poetry

COPY . .

RUN poetry install --only main

ENV ENV=production

CMD ["poetry", "run", "uvicorn", "--host=0.0.0.0", "--port=8000", "--reload", "app.main:app"]
