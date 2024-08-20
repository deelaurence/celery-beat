from django.urls import path
from .views import *

urlpatterns=[
    path("backup_data/", backup_data),
]