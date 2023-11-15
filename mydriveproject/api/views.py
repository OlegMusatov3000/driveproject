'''
views.py - Module containing Django views for handling Google Drive documents.

This module defines API views for creating and downloading Google Drive
documents
using the GoogleDriveManager. The views use the Django Rest Framework
decorators
to specify the HTTP methods they respond to.

Functions:
- create_google_drive_document_view: API view to create a new Google Drive
document.
- download_google_drive_document_view: API view to download a Google Drive
document.

Dependencies:
- Django: The web framework for building the views.
- rest_framework.decorators: Decorators for defining the API views.
- rest_framework.response: Response object for API responses.
- urllib.parse.quote: Function for URL encoding.

Submodules:
- managers.GoogleDriveManager: Manager class for interacting with Google Drive.

'''
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import quote

from .managers import GoogleDriveManager


@api_view(['POST'])
def create_google_drive_document_view(request):
    '''
    API view to create a new Google Drive document.

    Parameters:
    - request: The HTTP request object containing data and metadata.

    Returns:
    A Response object with a JSON indicating success and the created file ID.
    '''
    data = request.data.get('data', '')
    name = request.data.get('name', '')
    file_id = GoogleDriveManager().create_google_drive_document(data, name)
    return Response({'success': True, 'file_id': file_id})


@api_view(['GET'])
def download_google_drive_document_view(request, file_id):
    '''
    API view to download a Google Drive document.

    Parameters:
    - request: The HTTP request object.
    - file_id: The ID of the Google Drive document to be downloaded.

    Returns:
    A Django HttpResponse object with the document content
    and necessary headers.
    '''
    file_content, file_name = (
        GoogleDriveManager().download_google_drive_document(file_id)
    )

    quoted_file_name = quote(file_name)

    response = HttpResponse(file_content, content_type=(
        'application/vnd.openxmlformats-officedocument'
        '.wordprocessingml.document'
    ))
    response['Content-Disposition'] = (
        f'attachment; filename={quoted_file_name}.docx'
    )

    return response
