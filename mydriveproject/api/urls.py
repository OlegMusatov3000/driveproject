from django.urls import path

from .views import create_google_drive_document, download_google_drive_document

app_name = 'api'


urlpatterns = [
    path(
        'create_document/',
        create_google_drive_document,
        name='create_document'),
    path(
        'download_document/<slug:file_id>',
        download_google_drive_document,
        name='download_document')
]
