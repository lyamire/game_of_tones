## Description
Project name: 'Game of Notes: take your musical throne'
Quiz can consist of 1 - 5 rounds.
You have 40 seconds to answer the question.
## Installation

```shell
python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
python manage.py createsuperuser
```

Commands to create a database (from `psql`):
```sql
CREATE USER quiz WITH PASSWORD 'quiz' CREATEDB;
CREATE DATABASE quiz OWNER quiz;
GRANT ALL PRIVILEGES ON DATABASE quiz TO quiz;
```

## Run

```shell
python manage.py migrate
python manage.py runserver
```
