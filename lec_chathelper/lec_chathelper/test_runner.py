from django.test.runner import DiscoverRunner
from django.db import connection
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class ExampleTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
      databases = super().setup_databases(**kwargs)

      with open(os.path.join(CURRENT_DIR, "test/chat_test_db.sql")) as f:
        ddl_statement = f.read()

      with connection.cursor() as cursor:
        cursor.execute(ddl_statement)
      
      return databases