import os

TEST_DB_URL = os.environ.get('DATABASE_URL_DEV')
PRODUCTION_DB_URL = os.environ.get('DATABASE_URL_TEST')
