from __future__ import print_function
from celery import shared_task
import os
import subprocess
from datetime import datetime
import dropbox
from dotenv import load_dotenv
load_dotenv()



from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
print(DROPBOX_ACCESS_TOKEN)

@shared_task
def backup_postgres_and_upload(database_name, user, password, host, port, backup_dir):
    # Step 1: Perform the database backup
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = f"./{database_name}_backup_{timestamp}.sql"
    backup_path = os.path.join(backup_dir, backup_file)

    dump_cmd = f"PGPASSWORD={password} pg_dump -U {user} -h {host} -p {port} {database_name} > {backup_path}"
    subprocess.run(dump_cmd, shell=True, check=True)

    # Step 2: Upload the backup to Dropbox
    upload_to_dropbox(backup_path)

    # Optional: Remove the local backup file after upload
    os.remove(backup_path)

def upload_to_dropbox(file_path):
    # Create a Dropbox client
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

    # Upload the backup file to Dropbox
    with open(file_path, 'rb') as f:
        dbx.files_upload(f.read(), f"/{os.path.basename(file_path)}")

    print(f"Backup uploaded to Dropbox: {file_path}")


#perform the operation
# result = backup_postgres_and_upload.apply_async(
#             kwargs={
#                 'database_name': os.environ.get('DATABASE_NAME1'),
#                 'user': os.environ.get('DATABASE_USER'),
#                 'password': os.environ.get('DATABASE_PASSWORD'),
#                 'host': os.environ.get('DATABASE_HOST'),
#                 'port': 5432,
#                 'backup_dir': '.'
#             }
#         )
#         # Wait for the task to complete
# result.get(timeout=2000)


# print(result)