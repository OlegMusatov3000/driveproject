from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import quote

from .managers import GoogleDriveManager


@api_view(['POST'])
def create_google_drive_document_view(request):
    data = request.data.get('data', '')
    name = request.data.get('name', '')
    file_id = GoogleDriveManager().create_google_drive_document(data, name)
    return Response({'success': True, 'file_id': file_id})


@api_view(['GET'])
def download_google_drive_document_view(request, file_id):
    file_content, file_name = (
        GoogleDriveManager().download_google_drive_document(file_id)
    )

    # Кодируем русские символы в URL-кодировке
    quoted_file_name = quote(file_name)

    response = HttpResponse(file_content, content_type=(
        'application/vnd.openxmlformats-officedocument'
        '.wordprocessingml.document'
    ))
    response['Content-Disposition'] = (
        f'attachment; filename={quoted_file_name}.docx'
    )

    return response
