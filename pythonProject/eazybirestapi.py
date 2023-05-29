import requests

eazybi_url = 'http://jira.tafzs.com:8080/plugins/servlet/eazybi'
jira_username = 'fayaz'
jira_password = '123456789'
csv_file_path = 'jiraworklogdata.csv'
data = {
    'name': 'My CSV Data Source',
    'file_type': 'csv'
}
response = requests.post(f'{eazybi_url}/create_datasource', auth=(jira_username, jira_password), json=data)
if response.status_code != 200:
    print(f'Failed to create new datasource status code: {response.status_code}.')
    exit()

datasource_id = response.json().get('id')

files = {'file': open(csv_file_path, 'rb')}
response = requests.post(f'{eazybi_url}/import_datasource/{datasource_id}', auth=(jira_username, jira_password), files=files)
if response.status_code != 200:
    print(f'Failed to upload csv file to eazyBI status code : {response.status_code}.')
    exit()

print('csv file uploaded successfully')
