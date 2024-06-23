import requests
import xml.etree.ElementTree as ET

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def post_role_splunk(splunk_url, username,password, app_code):
    try:
        data = {
            'defaultApp': app_code,
            'name': f'ppod-dev-qa-{app_code}',
            'srchDiskQuota': 500,
            'srchIndexesAllowed': app_code,
            'srchIndexesDefault': app_code,
            'imported_roles': 'user'
        }

        response = requests.post(splunk_url, data=data, auth=(username,password), verify=False)

        response.raise_for_status()

        return response
    
    except requests.exceptions.RequestException as e:

        return e.response



if __name__=="__main__":
    splunk_host = 'splunk_host'

    username = "admin"
    password = "changeme"

    app_code = "1-3321-321"

    url=f"https://{splunk_host}:8089/services/authorization/roles"

    response = post_role_splunk(url, username, password, app_code)


    if response.status_code==201:
        print("Успешно создано")
    else:
        print("Ошибка. Подробности: \n"+response.text)