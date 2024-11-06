# Currencies
The backend API service for storing and managing currencies.

## Quick start
Create the configuration/**.env** file:
```env
DB_URL="postgresql+psycopg://test:test@db/test"
LOGS_PATH="logs/logs.txt"
SECRET_KEY= # openssl rand --hex 32
```
Create the configuration/**.env.db** file:
```env
POSTGRES_DB=test
POSTGRES_USER=test
POSTGRES_PASSWORD=test
```
Run Docker containers:
```bash
ENV=production ENV_FILE=./configuration/.env docker-compose up --build
```
Register the first admin user manually inside the backend docker:
```bash
poetry run python manage.py create-admin "admin@mail.com" "password"
```

## Environment variables

**ENV**
> Based on this value, the configuration will load a specific .env file from the configuration folder.\
Available values: **production** (.env), **development** (.env.dev), **test** (.env.test)

**DB_URL**
> URL of the database

**LOGS_PATH**
> Path to the file for writing logs

**SECRET_KEY**
> The minimum length is 32 characters. Generate one using `openssl rand --hex 32`.

**ALGORITHM** / optional
> JWT algorithm, by default "HS256"

**ACCESS_TOKEN_EXPIRE_MINUTES** / optional
> JWT lifetime, by default "15"

## Testing
Run a PostgreSQL Docker container:
```bash
docker run -d -p 5100:5432 -e POSTGRES_DB=test -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test postgres
```
Create the configuration/**.env.test** file:
```env
DB_URL="postgresql+psycopg://test:test@localhost:5100/test"
SECRET_KEY= # openssl rand --hex 32
LOGS_PATH="logs/logs.test.txt"
```
Install all dependencies:
```bash
poetry install --no-root
```
Run pytest: (The ENV variable will be set to 'test' even if another value was previously exported)
```bash
poetry run pytest
```

## Migrations
Activate the virtual environment and set the ENV:
```bash
poetry shell
export ENV=development
```
Create a migration file:
```bash
alembic revision --autogenerate -m "message"
```
Apply the latest migrations:
```bash
alembic upgrade head
```

## Scripts
Activate the virtual environment and set the ENV:
```bash
poetry shell
export ENV=development
```
**Create user**:
```bash
python manage.py create-user "email" "password"
```
**Create admin**:
```bash
python manage.py create-admin "email" "password"
```
**Load mock currencies**:
```bash
python manage.py create-mock-currs
```
