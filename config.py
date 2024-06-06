# Author: Shidul Islam
# Date: 10-11-2023
# */

from dotenv import load_dotenv
import os
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

USER_SECRET = os.getenv("USER_SECRET")
VENDOR_SECRET = os.getenv("VENDOR_SECRET")
ADMIN_SECRET = os.getenv("ADMIN_SECRET")
SUPER_ADMIN_SECRET = os.getenv("SUPER_ADMIN_SECRET")

API_BASE_URL = os.getenv("API_BASE_URL")

AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_S3_ACCESS_KEY = os.getenv("AWS_S3_ACCESS_KEY")
AWS_S3_SECRET_KEY = os.getenv("AWS_S3_SECRET_KEY")

EMAIL_ID = os.getenv("EMAIL_ID")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
