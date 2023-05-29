import requests
import csv

jira_url = 'http://jira.tafzs.com:8080/rest/api/2'
username = 'fayaz'
password = '123456789'

jql_query = 'project in ("External Legal Project") AND "Customer company name" in ("Angular Directions") AND worklogDate >= startOfMonth(-1M) AND worklogDate <= endOfMonth(-1M) AND worklogAuthor in (fayaz, navi, likitha)'

headers = {
    'Accept': 'application/json'
}
auth = (username, password)

issues = requests.get(jira_url + '/search', params={'jql': jql_query}, headers=headers, auth=auth).json()['issues']

with open('worklog.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Issue Key', 'Request Type', 'Author', 'Time Spent', 'Start Time', 'Comment'])

for issue in issues:
    issue_key = issue['key']
    request_type = issue['fields']['issuetype']['name']
    worklogs = requests.get(jira_url + '/issue/' + issue_key + '/worklog', headers=headers, auth=auth).json()['worklogs']
    for worklog in worklogs:
        with open('worklog.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                issue_key,
                request_type,
                
                worklog['author']['name'],
                worklog['timeSpent'],
                worklog['started'],
                worklog['comment']
            ])
