# Currency Converter
Full stack project that includes two servers:\
[**Backend**](./backend/README.md) allows you to manipulate currencies in the database\
[**Frontend**](./frontend/README.md) is single-page app for viewing currency values

## Fast Start
First at all you need to populate ./backend/configuration/.env
```env
DB_URL="postgresql+psycopg://deadpool:x-force@db/app"
LOGS_PATH="logs/logs.txt"

SECRET_KEY="your-super-secret-key" # openssl rand --hex 32
```
Also, update .env.db at the root of the project
```env
POSTGRES_USER="deadpool"
POSTGRES_PASSWORD="x-force"
POSTGRES_DB="app"
```
Then you can run containers
```bash
docker-compose up --build
```
The final step is to insert mock currencies into the database. Go to the backend container, and inside its terminal, run this command:
```bash
poetry run manage.py create-mock-currs
```
Finally, open the browser and go to http://localhost:8000 (frontend) or http://localhost:8080 (backend)
