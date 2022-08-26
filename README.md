## Setup packages 
### Install Psycopg2
```sha
sudo apt-get install libpq-dev
sudo apt-get install python3-psycopg2
```  
### Install Virtual Environment 

```sha
sudo apt-get install python3-venv
```


## Setup

Install the dependencies:
```sh
$ pip install -r requirements.txt
```

Create .env file with following dependencies:
```sh
APPLICANT_BOT_API_TOKEN=
SUPPLIER_BOT_API_TOKEN=
SECRET_KEY=
ALLOWED_HOSTS=*

DB_HOST=localhost
DB_PORT=5432
DB_NAME=
DB_USER=
DB_PASSWORD=
ONE_C_SERVER_URL=
ONE_C_SERVER_LOGIN=
ONE_C_SERVER_PASSWORD=
```

Once `pip` has finished downloading the dependencies:
```sh
$ python manage.py migrate
$ python manage.py makemigrations app
$ python manage.py migrate app 0001
```
Create Django user:
```sh
$ python manage.py createsuperuser
```
 
Collect static files
```sh
$ python manage.py collectstatic
```

