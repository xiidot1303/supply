import os
from dotenv import load_dotenv

load_dotenv(os.path.join(".env"))

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

# Postgres db informations
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# Telegram bot tokens
APPLICANT_BOT_API_TOKEN = os.environ.get("APPLICANT_BOT_API_TOKEN")
SUPPLIER_BOT_API_TOKEN = os.environ.get("SUPPLIER_BOT_API_TOKEN")

# Url
STORAGE_URL = os.environ.get("ONE_C_SERVER_URL")+'/siyob_snab_new/hs/purchase/remains/'
CREATING_STATEMENT_URL = os.environ.get("ONE_C_SERVER_URL")+'/siyob_snab_new/hs/purchase/order/'
ONE_C_SERVER_LOGIN = os.environ.get("ONE_C_SERVER_LOGIN")
ONE_C_SERVER_PASSWORD = os.environ.get("ONE_C_SERVER_PASSWORD")
