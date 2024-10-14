# Backend

## Enviroment variables

### ENV
> Based on this value, the configuration will load a specific .env file from the configuration folder.\
Available values: **production** (.env), **development** (.env.dev), **test** (.env.test)

### DB_URL
> URL of the database

### LOGS_PATH
> Path to the file for writing logs

### SECRET_KEY
> The minimum length is 32 characters, generate with `openssl rand --hex 32`.

### ALGORITHM / optional
> JWT algoritm, by default "HS256"
### ACCESS_TOKEN_EXPIRE_MINUTES / optional
> JWT token lifetime, by default "15"

## Testing
Run a postgresql docker
```bash
docker run -d -p 5100:5432 -e POSTGRES_DB=test -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test postgres
```
Create the configuration/**.env.test** file
```env
DB_URL="postgresql+psycopg://test:test@localhost:5100/test"
SECRET_KEY= # openssl rand --hex 32
LOGS_PATH="logs/logs.test.txt"
```
Run pytest (ENV will be overridden to 'test' even if it was exported with a different value)
```bash
poetry run pytest
```

## Migrations
To create migration file:
```bash
poetry run alembic revision --autogenerate -m "message"
```
To apply migrations:
```bash
poetry run alembic upgrade head
```

## Logs

### Logger Midlleware
Generates a request ID that binds to the logger and attaches to each request for later use.
Middleware logs every request, response, and server exception.

### Logger Depends
To access the logger from a request, use get_logger() or the LoggerDepends type from app/logger.py.

## Create Admin
First admin must be created manually
```bash
poetry run python manage.py create-admin email@example.com your-password
```
