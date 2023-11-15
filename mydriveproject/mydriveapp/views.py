import os
import json
from django.http import JsonResponse, HttpResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.views.decorators.csrf import csrf_exempt
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload


@csrf_exempt
def create_google_drive_document(request):
    if request.method == 'POST':
        # Получаем данные из тела POST запроса в формате JSON
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        data = body_data.get('data', '')
        name = body_data.get('name', '')

        # Замените значения на свои
        token_path = '/Users/olegmusatov/Dev/driveproject/token.json'
        credentials_path = '/Users/olegmusatov/Dev/driveproject/mydriveproject/credentials.json'

        # Подставьте свой идентификатор проекта и путь к файлу credentials.json
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = None

        # Загрузка существующих учетных данных, если они есть
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)

        # Если учетных данных нет или они устарели, запускаем процесс аутентификации
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Сохраняем учетные данные для следующего выполнения
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        # Создаем документ в Google Drive
        drive_service = build('drive', 'v3', credentials=creds)
        file_metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.document'}

        # Создаем файл в памяти
        file_stream = io.BytesIO(data.encode('utf-8'))

        # Используем MediaIoBaseUpload для передачи файла в виде данных
        media = MediaIoBaseUpload(file_stream, mimetype='text/plain', resumable=True)

        # Создаем файл в Google Drive
        created_file = drive_service.files().create(body=file_metadata, media_body=media).execute()

        # Возвращаем ответ с дополнительной информацией
        return JsonResponse({
            'success': True,
            'file_id': created_file['id'],
        })

    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def download_google_drive_document(request, file_id):
    if request.method == 'GET':
        # Замените значения на свои
        token_path = '/Users/olegmusatov/Dev/driveproject/token.json'
        credentials_path = '/Users/olegmusatov/Dev/driveproject/mydriveproject/credentials.json'

        # Подставьте свой идентификатор проекта и путь к файлу credentials.json
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = None

        # Загрузка существующих учетных данных, если они есть
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)

        # Если учетных данных нет или они устарели, запускаем процесс аутентификации
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Сохраняем учетные данные для следующего выполнения
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        # Загружаем файл из Google Drive
        drive_service = build('drive', 'v3', credentials=creds)
        file_metadata = drive_service.files().get(fileId=file_id).execute()

        # Загружаем файл из Google Drive
        request = drive_service.files().export(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Получаем имя файла из метаданных
        file_name = file_metadata.get('name', 'downloaded_document.docx')

        # Возвращаем файл в качестве ответа с правильным именем
        response = HttpResponse(file_stream.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={file_name}.docx'
        return response

    else:
        return JsonResponse({'error': 'Invalid request method'})