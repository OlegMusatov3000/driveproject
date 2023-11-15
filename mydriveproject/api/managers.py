'''
GoogleDriveManager - A class for managing interactions with Google Drive.

This module provides a simple interface for creating and downloading Google
Drive documents.
It utilizes the Google Drive API and requires authentication through OAuth 2.0.

Classes:
    GoogleDriveManager: Manages Google Drive interactions, including document
    creation and download.

Methods:
    - __init__(self): Initializes the GoogleDriveManager with authentication
    credentials.
    - get_credentials(self): Retrieves and refreshes OAuth 2.0 credentials for
    Google Drive.
    - create_google_drive_document(self, data, name): Creates a new Google
    Drive document with the given data and name.
    - download_google_drive_document(self, file_id): Downloads a Google Drive
    document with the specified file ID.

Dependencies:
    - io
    - os
    - google_auth_oauthlib
    - google.auth.transport.requests
    - google.oauth2.credentials
    - googleapiclient.discovery
    - googleapiclient.http.MediaIoBaseUpload
    - googleapiclient.http.MediaIoBaseDownload
    - mydriveproject.settings (for TOKEN, CREDENTIALS, SCOPES)

Note:
    Ensure that the 'mydriveproject.settings' module is configured with valid
    TOKEN, CREDENTIALS, and SCOPES.

Usage:
    Instantiate the GoogleDriveManager class and use its methods to interact
    with Google Drive.
'''
import io
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

from mydriveproject.settings import TOKEN, CREDENTIALS, SCOPES


class GoogleDriveManager:
    '''
    GoogleDriveManager - A class for managing interactions with Google Drive.

    This class encapsulates functionalities related to Google Drive, such as
    authentication,
    document creation, and document download using the Google Drive API.

    Attributes:
        creds (Credentials): OAuth 2.0 credentials for authenticating with
        Google Drive.

    Methods:
        - __init__(self): Initializes the GoogleDriveManager with
        authentication credentials.
        - get_credentials(self): Retrieves and refreshes OAuth 2.0 credentials
        for Google Drive.
        - create_google_drive_document(self, data, name): Creates a new Google
        Drive document with the given data and name.
        - download_google_drive_document(self, file_id): Downloads a Google
        Drive document with the specified file ID.

    Dependencies:
        - io
        - os
        - google_auth_oauthlib
        - google.auth.transport.requests
        - google.oauth2.credentials
        - googleapiclient.discovery
        - googleapiclient.http.MediaIoBaseUpload
        - googleapiclient.http.MediaIoBaseDownload
        - mydriveproject.settings (for TOKEN, CREDENTIALS, SCOPES)

    Note:
        Ensure that the 'mydriveproject.settings' module is configured with
        valid TOKEN, CREDENTIALS, and SCOPES.
    '''
    def __init__(self):
        '''
        Initialize the GoogleDriveManager.

        This constructor sets up the GoogleDriveManager instance with the
        necessary authentication credentials.
        If valid credentials are not present, it triggers the OAuth 2.0
        authentication process.
        The resulting credentials are stored in the 'creds' attribute.

        Args:
            None

        Returns:
            None
        '''
        self.creds = self.get_credentials()

    def get_credentials(self):
        '''
        Retrieve and refresh OAuth 2.0 credentials for Google Drive.

        This method checks if valid credentials are stored locally. If not, it
        initiates the OAuth flow
        to obtain and store new credentials. If existing credentials are
        expired, it attempts to refresh them.

        Args:
            None

        Returns:
            Credentials: OAuth 2.0 credentials for authenticating with Google
            Drive.
        '''
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
        '''
        Create a new Google Drive document.

        This method creates a new Google Drive document with the provided data
        and name.
        The document is of MIME type 'application/vnd.google-apps.document'.

        Args:
            data (str): The content of the document.
            name (str): The name of the document.

        Returns:
            str: The ID of the created document.
        '''
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
        '''
        Download a Google Drive document.

        This method downloads the Google Drive document with the specified
        file ID.
        It exports the document in the format
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'.

        Args:
            file_id (str): The ID of the document to be downloaded.

        Returns:
            tuple: A tuple containing the downloaded data (bytes) and the name
            of the downloaded document.
        '''
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
