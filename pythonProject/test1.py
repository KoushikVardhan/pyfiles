import pandas as pd
import requests

df = pd.read_csv('jiraworklogdata.csv')

url = 'http://jira.tafzs.com:8080/rest/api/2/dashboard/10113'

auth = ('fayaz', '123456789')

response = requests.put(url, auth=auth, json=df, headers={'Content-Type': 'application/json'})

if response.status_code == 200:
    print("successfull")
else:
    print("Failed")
    