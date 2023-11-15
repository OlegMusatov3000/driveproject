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
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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

schema_view = get_schema_view(
    openapi.Info(
        title='Drive Project',
        default_version='v1',
        description=(
            'Документация для приложения api проекта Drive Project'
        ),
        contact=openapi.Contact(email='olegmusatov97@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
)

urlpatterns += [
    re_path(
        r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
