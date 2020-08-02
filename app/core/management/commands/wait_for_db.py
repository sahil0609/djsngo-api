import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """wait for db until db is not avaialble """
    def handle(self, *args, **options):
        self.stdout.write('waiting for db..')
        db_conn=None
        
        while not db_conn:
            
            try:
                conn=connections['default']
                conn.cursor()
                db_conn=True
            except OperationalError:
                self.stdout.write('sleep for 1 sec')
                time.sleep(1)
            except Exception as e:
                self.stdout.write("something happened")
                self.stdout.write(str(e))
                break
                
        print(db_conn)
        self.stdout.write(self.style.SUCCESS('Database connected'))