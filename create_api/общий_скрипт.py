from flask import Flask, request, jsonify
import time
import requests
import xml.etree.ElementTree as ET
import socket

app = Flask(__name__)


@app.route('/orders', methods=['POST'])
def handle_post():
    try:
        data = request.json
        splunk_host = 'https://splunk_host:8089'
        username = "admin"
        password = "changeme"
        app_code = data.get('code')
        index = app_code
        zone = {
            'dev': 'dev',
            'prod': 'prod',
            'test': 'test'
        }
        role = {
            'Тестировщик': 'qa',
            'Разработчик': 'developer',
            'Руководитель разработки': 'devlead',
            'IT-Лидер': 'it-lead',
            'Бизнес-пользователь': 'pbu',
            'Администратор приложения': 'admin-app',
            'ТУЗ приложения': 'service'
        }
        role_name = f"{zone['dev']}-{role['Разработчик']}-{app_code}"
        app_name = app_code
        return_data = {}

        create_app_response = post_splunk_app(splunk_server=splunk_host, username=username, password=password, app_code=app_code, app_name=app_name)

        if create_app_response.status_code==201:
            create_index_response = post_splunk_index(splunk_server=splunk_host, index=index, username=username,password=password)
            if create_index_response['status_code']==201:
                create_HEC_response = set_HEC_splunk(index=index, name=app_code, username=username, password=password)
                if create_HEC_response['status_code']==201:
                    create_role_response = post_role_splunk(splunk_server=splunk_host, username=username, password=password, name=role_name, app_code=app_code)
                    if create_role_response.status_code==201:
                        return_data['SPLUNK_TOKEN'] = create_HEC_response['token']
                        return_data['SPLUNK_INDEX'] = create_index_response['index']
                        return_data['SPLUNK_URL'] = f'https://splunk_url:15000/services/collector/event'
        return jsonify(return_data)
        
    except Exception as e:
        response_data = {
            'timestamp': int(time.time()*1000),
            'status': 400,
            'error': 'Bad Request',
            'exception': str(type(e).__name__),
            'message': str(e),
            'path': request.path
        }
        return jsonify(response_data), 400

def post_splunk_app(splunk_server,username,password,app_code, app_name):
    try:
        data = {
            'author': app_code,
            'configured': True,
            'filename': False,
            'label': app_name,
            'name': app_code,
            'version': "1.0.0",
            'visible': True
        } 

        create_response = requests.post(f'{splunk_server}/services/apps/local',data=data, auth=(username,password), verify=False)

        create_response.raise_for_status()

        return create_response
    
    except requests.exceptions.RequestException as e:

        return e.response
    
def post_splunk_index(splunk_server, index, username, password):
    try:
        index_data = {
            "name": index,
            "homePath": f"$SPLUNK_DB/{index}/db",
            "coldPath": f"$SPLUNK_DB/{index}/colddb",
            "thawedPath": f"$SPLUNK_DB/{index}/thaweddb",
            "maxTotalDataSizeMB": 500
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
            'status_code': create_response.status_code,
            'response': create_response
        }
        return data
    
    except requests.exceptions.RequestException as e:
        data = {
            'status_code': e.response.status_code,
            'response': e.response
        }
        return data

def set_HEC_splunk(index,name, username, password):
    try:
        data = {
            'disabled': 0,
            'index': index,
            'name': name,
            'indexes': index,
            'sourcetype': index
        }
        create_response = requests.post('https://splunk_host:8089/services/data/inputs/http', data=data, auth=(username,password), verify=False)
        create_response.raise_for_status()

        root = ET.fromstring(create_response.text)
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            's': 'http://dev.splunk.com/ns/rest'
        }
        for entry in root.findall('atom:entry', namespaces):
            title = entry.find('atom:title', namespaces).text
            token = entry.find('.//s:key[@name="token"]', namespaces).text
            link = entry.find('atom:link[@rel="alternate"]', namespaces).attrib['href']
            result={
                'title': title,
                'token': token,
                'link': link,
                'status_code': create_response.status_code,
                'response': create_response.text
            }
        return result
    except requests.exceptions.RequestException as e:
        result = {
            'status_code': e.response.status_code,
            'response': e.response.text
        }

def post_role_splunk(splunk_server, username,password, name, app_code):
    try:
        data = {
            'defaultApp': app_code,
            'name': name,
            'srchDiskQuota': 500,
            'srchIndexesAllowed': app_code,
            'srchIndexesDefault': app_code,
            'imported_roles': 'user'
        }

        response = requests.post(f'{splunk_server}/services/authorization/roles', data=data, auth=(username,password), verify=False)

        response.raise_for_status()

        return response
    
    except requests.exceptions.RequestException as e:

        return e.response

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")