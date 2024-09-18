# Currency Converter
Full stack project that includes two servers:\
[**Backend**](./backend/README.md) allows you to manipulate with currencies in the database\
[**Frontend**](./frontend/README.md) servers single page app for looking currencies values

## Fast Start
First at all you need to populate ./backend/configuration/.env
```bash
DB_URL="postgresql+psycopg://deadpool:x-force@db/app"
LOGS_PATH="logs/logs.txt"
SECRET_KEY="your-super-secret-key"
```
Also .env.db at root of the project
```bash
POSTGRES_USER="deadpool"
POSTGRES_PASSWORD="x-force"
POSTGRES_DB="app"
```
Then you can run containers
```bash
docker-compose up --build
```
The last part is to insert mock currencies into the database, go to the backend container and inside its terminal run this
```bash
poetry run manage.py create-mock-currs
```
Finnaly, go to the browser!
