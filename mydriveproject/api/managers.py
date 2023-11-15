import io
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

from mydriveproject.settings import TOKEN, CREDENTIALS, SCOPES


class GoogleDriveManager:
    def __init__(self):
        self.creds = self.get_credentials()

    def get_credentials(self):
        creds = None
        if os.path.exists(TOKEN):
            creds = Credentials.from_authorized_user_file(TOKEN)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN, 'w') as token:
                token.write(creds.to_json())

        return creds

    def create_google_drive_document(self, data, name):
        drive_service = build('drive', 'v3', credentials=self.creds)
        file_metadata = {
            'name': name, 'mimeType': 'application/vnd.google-apps.document'
        }

        file_stream = io.BytesIO(data.encode('utf-8'))
        media = MediaIoBaseUpload(
            file_stream, mimetype='text/plain', resumable=True
        )

        created_file = drive_service.files().create(
            body=file_metadata, media_body=media
        ).execute()

        return created_file.get('id')

    def download_google_drive_document(self, file_id):
        drive_service = build('drive', 'v3', credentials=self.creds)
        file_metadata = drive_service.files().get(fileId=file_id).execute()

        request = drive_service.files().export(fileId=file_id, mimeType=(
            'application/vnd.openxmlformats-officedocument'
            '.wordprocessingml.document'
        ))
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        file_name = file_metadata.get('name', 'downloaded_document.docx')
        return file_stream.getvalue(), file_name
