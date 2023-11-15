from django.core.management.base import BaseCommand
from rest_framework.test import APIRequestFactory

from api.views import create_google_drive_document_view
from mydriveproject.settings import API_URL


class Command(BaseCommand):
    help = 'Create a new document and print the file_id'

    def handle(self, *args, **kwargs):
        factory = APIRequestFactory()

        # ANSI Escape Codes
        bold_start = '\033[1m'  # Начало выделения жирным шрифтом
        bold_end = '\033[0m'  # Завершение выделения

        # Попросим пользователя ввести название документа
        name = input('Введите название документа: ')

        # Попросим пользователя ввести содержание документа
        data = input('Введите содержание документа: ')

        # Создадим запрос к нашему API
        request = factory.post(
            '/api/create_google_drive_document/',
            {'name': name, 'data': data}, format='json'
        )

        # Вызовем метод создания документа
        response = create_google_drive_document_view(request)

        # Получим file_id из ответа
        file_id = response.data['file_id']

        # Выведем информацию в терминал
        print(
            f'\nУникальный идентификатор: {bold_start}{file_id}{bold_end}\n'
            '\nИспользуйте его для скачивания документа по адресу:\n'
            f'\n{API_URL}{bold_start}{file_id}{bold_end}\n'
        )
