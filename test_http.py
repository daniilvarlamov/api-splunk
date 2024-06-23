import requests
import json

# Параметры
splunk_host = "https://192.168.5.55:8088"
hec_token = "b0f7eaab-f3b0-45c0-9adc-3c233e1785c3"
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