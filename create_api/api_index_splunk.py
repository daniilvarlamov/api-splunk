import requests
import xml.etree.ElementTree as ET

# Конфигурация Splunk
splunk_server = "https://192.168.5.61:8089"
username = "admin"
password = "1q@3e4r"

# Аутентификация
auth_url = f"{splunk_server}/services/auth/login"
auth_response = requests.post(auth_url, data={"username": username, "password": password}, verify=False)

# Проверка успешности запроса
if auth_response.status_code != 200:
    print(f"Failed to authenticate. Status code: {auth_response.status_code}")
    print(auth_response.text)
    exit(1)

# Разбор XML-ответа
try:
    root = ET.fromstring(auth_response.text)
    session_key = root.find('sessionKey').text
except ET.ParseError:
    print("Failed to parse XML response")
    print(auth_response.text)
    exit(1)

# Заголовки с токеном
headers = {
    "Authorization": f"Splunk {session_key}"
}

# Данные для создания индекса
index_data = {
    "name": "my_new_index2",
    "homePath": "$SPLUNK_DB/my_new_index2/db",
    "coldPath": "$SPLUNK_DB/my_new_index2/colddb",
    "thawedPath": "$SPLUNK_DB/my_new_index2/thaweddb"
}

# Создание индекса в system local
create_index_url = f"{splunk_server}/servicesNS/admin/system/data/indexes"
create_response = requests.post(create_index_url, headers=headers, data=index_data, verify=False)

if create_response.status_code == 201:
    print("Index created successfully.")
else:
    print(f"Failed to create index. Status code: {create_response.status_code}")
    print(create_response.text)