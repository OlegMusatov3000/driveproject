import requests
import json

url = "http://localhost:8000/create_document/"
headers = {"Content-Type": "application/json"}

# Тело запроса
payload = {
    "data": "Hello world",
    "name": "test file"
}

# Преобразование в JSON и отправка POST-запроса
try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()  # Проверка на ошибки

    # Анализ JSON-ответа и получение ссылки на скачивание
    response_json = response.json()
    download_link = response_json.get("download_link")
    print(response_json)
    if download_link:
        print(f"Запрос успешно отправлен. Ссылка на скачивание: {download_link}")
    else:
        print("Сервер не вернул ссылку на скачивание.")
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.RequestException as err:
    print(f"An error occurred: {err}")
