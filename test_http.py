import requests
import json

# Параметры
splunk_host = "https://192.168.5.55:8088"
hec_token = "fd54a412-8f02-47bb-ae86-5e1bf8f22ddb"
hec_url = f"{splunk_host}/services/collector/event"


# Данные для отправки
event_data = {
    "event": {
        "message": "Test Event"
    }
}

# Заголовки запроса
headers = {
    "Authorization": f"Splunk {hec_token}",
    "Content-Type": "application/json",
    "host": "test_host",
    "source": "test_source"
}

try:
    # Выполнение POST-запроса
    response = requests.post(hec_url, headers=headers, data=json.dumps(event_data), verify=False)
    
    # Проверка статуса ответа
    response.raise_for_status()

    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e.response.text}")