from django.http import JsonResponse
from .tasks import backup_postgres_and_upload
from dotenv import load_dotenv
import os
load_dotenv()

# Create your views here.

def backup_data(request):
    try:
        # Trigger the task and wait for it to finish
        result = backup_postgres_and_upload.apply_async(
            kwargs={
                'database_name': os.environ.get('DATABASE_NAME'),
                'user': os.environ.get('DATABASE_USER'),
                'password': os.environ.get('DATABASE_PASSWORD'),
                'host': os.environ.get('DATABASE_HOST'),
                'port': 5432,
                'backup_dir': '.'
            }
        )
        # Wait for the task to complete
        result.get(timeout=2000)  # You can adjust the timeout as needed
        return JsonResponse({"message": f'The task with id {result.id} status is {result.status}'})
    except Exception as e:
        # Handle other potential exceptions
        return JsonResponse({'error': str(e)}, status=500)
