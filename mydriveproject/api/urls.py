'''
URL Configuration for the 'api' app.

- `create_document`: Endpoint for creating a Google Drive document.
- `download_document`: Endpoint for downloading a Google Drive document by
file ID.

Example:
    To create a new Google Drive document, make a POST request to
    '/api/create_document/'.
    To download a Google Drive document, make a GET request to
    '/api/download_document/<file_id>'.

'''
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
