import requests
import xml.etree.ElementTree as ET


def post_splunk_app(splunk_url,username,password,app_code, app_name):
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

        create_response = requests.post(splunk_url,data=data, auth=(username,password), verify=False)

        create_response.raise_for_status()

        return create_response
    
    except requests.exceptions.RequestException as e:

        return e.response



if __name__=="__main__":

    splunk_hosts = 'splunk_host'

    username = "admin"

    password = "changeme"

    app_name = "test_app"

    app_code = "1-3321-321"

    for splunk_host in splunk_hosts:
        splunk_url=f"https://{splunk_host}:8089/services/apps/local"

        response = post_splunk_app(splunk_url, username, password, app_code, app_name)

        if response.status_code==201:
            print("Успешно создано на узле:" + splunk_host)
        else:
            print("Ошибка. Подробности: \n"+response.text)