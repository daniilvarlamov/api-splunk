import requests
import xml.etree.ElementTree as ET


requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def set_HEC_splunk(http_inputs_url,index,name,sourcetype, username, password):
    try:
        data = {
            'disabled': 0,
            'index': index,
            'name': name,
            'indexes': index
        }
        create_response = requests.post(http_inputs_url, data=data, auth=(username,password), verify=False)
        create_response.raise_for_status()
        return create_response
    except requests.exceptions.RequestException as e:
        return e.response



def get_HEC_token_splunk(http_inputs_url,name, username, password):
    try:
        response = requests.get(http_inputs_url,  auth=(username, password), verify=False)
        root = ET.fromstring(response.text)
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            's': 'http://dev.splunk.com/ns/rest'
        }
        for entry in root.findall('atom:entry', namespaces):
            title = entry.find('atom:title', namespaces).text
            if title.__contains__(name):
                token = entry.find('.//s:key[@name="token"]', namespaces).text
                link = entry.find('atom:link[@rel="alternate"]', namespaces).attrib['href']
                result={
                    'title': title,
                    'token': token,
                    'link': link,
                    'status_code': response.status_code,
                    'response': response.text
                }


        return result
    except requests.exceptions.RequestException as e:
        return e.response


if __name__=="__main__":
    splunk_host = "https://deploy_host:8089"
    username = "admin"
    password = "changeme"
    index = "1-3321-321"
    name=index
    sourcetype=index
    http_inputs_url = f"{splunk_host}/services/data/inputs/http"

    set_response = set_HEC_splunk(http_inputs_url,index,name,sourcetype,username,password)
    if set_response.status_code==201:
        data = get_HEC_token_splunk(http_inputs_url,name, username, password)
        print(data['token'])
    else:
        root = ET.fromstring(set_response.text)
        message = root.find(".//msg").text
        print("Ошибка при создании токена. Код: " + str(set_response.status_code)+'\n'+"Сообщение: "+ message)
