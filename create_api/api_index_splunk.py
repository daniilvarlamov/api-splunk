import requests
import xml.etree.ElementTree as ET

# Конфигурация Splunk
splunk_server = "https://splunk_host:8089"
username = "admin"
password = "changeme"
index = "my_new_index2"


index_data = {
    "name": index,
    "homePath": f"$SPLUNK_DB/{index}/db",
    "coldPath": f"$SPLUNK_DB/{index}/colddb",
    "thawedPath": f"$SPLUNK_DB/{index}/thaweddb"
}

# Создание индекса в system local
create_index_url = f"{splunk_server}/servicesNS/admin/system/data/indexes"
create_response = requests.post(create_index_url, auth=(username,password), data=index_data, verify=False)


create_response.raise_for_status()

root = ET.fromstring(fr"{create_response.text}")
ns = {'atom': 'http://www.w3.org/2005/Atom'}
index_title = root.find('atom:entry/atom:title', ns).text
data = {
    'index': index_title,
    'status_code': create_response.status_code
}


print(data)