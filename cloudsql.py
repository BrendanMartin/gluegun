"""
Launch the Google Cloud SQL Proxy:
> python cloudsql.py

Requires .env to be set up with proper credentials,
as well as having credentials.json saved from Google Cloud Admin.
"""

import os
import subprocess

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

conn_name = os.getenv('CLOUD_SQL_INSTANCE_CONNECTION_NAME')
credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

subprocess.call([r'%HOME%\cloudsql\cloud_sql_proxy.exe',
                 f'-instances={conn_name}=tcp:5433',        # NOTE: port is 5433 not default 5432
                 f'-credential_file={credentials}'],
                shell=True)
