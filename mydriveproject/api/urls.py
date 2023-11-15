from django.urls import path

from .views import (
    create_google_drive_document_view, download_google_drive_document_view
)

app_name = 'api'


urlpatterns = [
    path(
        'create_document/',
        create_google_drive_document_view,
        name='create_document'),
    path(
        'download_document/<slug:file_id>',
        download_google_drive_document_view,
        name='download_document')
]
