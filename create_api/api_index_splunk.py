import requests
import xml.etree.ElementTree as ET


requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def post_splunk_app(splunk_url,username,password,app_code):
    try:
        data = {
            'datatype': 'event',
            'maxTotalDataSizeMB': 500,
            'name': app_code
        }

        create_response = requests.post(splunk_url,data=data, auth=(username,password), verify=False)

        create_response.raise_for_status()

        return create_response
    
    except requests.exceptions.RequestException as e:

        return e.response



if __name__=="__main__":

    splunk_hosts = ['192.168.5.133', '192.168.5.68']

    username = "admin"
    password = "1q@3e4r"

    app_code = "1-3321-321"

    for splunk_host in splunk_hosts:
        splunk_url=f"https://{splunk_host}:8089/servicesNS/admin/{app_code}/data/indexes"

        response = post_splunk_app(splunk_url, username, password, app_code)

        if response.status_code==201:
            print("Успешно создано на узле:" + splunk_host)
        else:
            print("Ошибка. Подробности: \n"+response.text)

