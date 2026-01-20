# Configuration file for database connections
# ВАЖНО: Для GitHub используйте переменные окружения вместо hardcoded значений!

import os
from dotenv import load_dotenv

load_dotenv()

# MySQL Configuration (Sakila database)
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'sakila')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))

# MongoDB Configuration
MONGODB_URL_READ = os.getenv(
    'MONGODB_URL_READ',
    'mongodb://ich1:password@mongo.itcareerhub.de/?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich'
)
MONGODB_URL_EDIT = os.getenv(
    'MONGODB_URL_EDIT',
    'mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit'
)
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'ich')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION', 'final_project_010825_daryna_abalmasova')

# Search Parameters
RESULTS_PER_PAGE = 10
STATS_LIMIT = 5

# Logging
LOG_FILE = 'search_app.log'
