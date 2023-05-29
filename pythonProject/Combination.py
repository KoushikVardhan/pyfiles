import requests
import csv
import re

jira_url = 'http://jira.tafzs.com:8080/rest/api/2'
username = 'fayaz'
password = '123456789'

jql_query = 'project in ("External Legal Project") AND "Customer company name" in ("Angular Directions") AND worklogDate >= startOfMonth(-1M) AND worklogDate <= endOfMonth(-1M) AND worklogAuthor in (fayaz, navi, likitha)'

headers = {
    'Accept': 'application/json'
}
auth = (username, password)

issues = requests.get(jira_url + '/search', params={'jql': jql_query}, headers=headers, auth=auth).json()['issues']

with open('combination.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Issue Key', 'Request Type', 'Author', 'Time Spent', 'Start Time', 'Comment'])

for issue in issues:
    issue_key = issue['key']
    request_type = issue['fields']['issuetype']['name']
    worklogs = requests.get(jira_url + '/issue/' + issue_key + '/worklog', headers=headers, auth=auth).json()['worklogs']
    for worklog in worklogs:
        comment = worklog['comment']
        pattern = r"(\w+):(\d+):(\d+):(\w+)"
        match = re.search(pattern, comment)
        if match:
            valuetax = int(match.group(3))
            valueamount = int(match.group(2))
        elif match:
            valuetax = int(match.group(3))
        elif match:
            valueamount = int(match.group(2))
        else:
            valueamount = 0,
            valuetax = 0

        with open('combination.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                issue_key,
                request_type,
                worklog['author']['name'],
                worklog['timeSpent'],
                worklog['started'],
                worklog['comment'],
                valuetax,
                valueamount
            ])
