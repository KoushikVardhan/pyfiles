from typing import Tuple

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

with open('combination1.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['Issue Key', 'Request Type', 'Author', 'Time Spent', 'Start Time', 'Comment'])

for issue in issues:
    issue_key = issue['key']
    request_type = issue['fields']['issuetype']['name']
    worklogs = requests.get(jira_url + '/issue/' + issue_key + '/worklog', headers=headers, auth=auth).json()[
        'worklogs']
    for worklog in worklogs:
        amount1 = 250,
        amount2 = 200,
        amount3 = 100,
        weeks, days, hours, minutes = 0, 0, 0, 0
        for part in worklog['timeSpent'].split():
            if part.endswith('w'):
                weeks = int(part[:-1])
            elif part.endswith('d'):
                days = int(part[:-1])
            elif part.endswith('h'):
                hours = int(part[:-1])
            elif part.endswith('m'):
                minutes = int(part[:-1])
        total_minutes = weeks * 7 * 24 * 60 + days * 24 * 60 + hours * 60 + minutes
        comment = worklog['comment']
        pattern = r"(\w+):(\d+):(\d+):(\w+)"
        # Extract integer values using regular expression
        match = re.search(pattern, comment)
        if match and re.search("FIXED", comment):
            valueamount = int(match.group(2))
            valuetax = int(match.group(3))

        if worklog['author']['name'] == 'fayaz':
            x = amount1 * total_minutes,
            y = sum(x) / 60,
            valueamount = y
        if worklog['author']['name'] == "likitha":
            x = amount2 * total_minutes,
            y = sum(x) / 60,
            valueamount = y
        if worklog['author']['name'] == "Navi":
            x = amount3 * total_minutes,
            y = sum(x) / 60,
            valueamount = y


        with open('combination1.csv', 'a', newline='') as file:
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
with open('combination1.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    with open('combination1.csv', 'r', newline='') as file:
        writer = csv.writer(file)

        for row in reader:
            if 'EXCLUDE' not in row[2]:
                writer.writerow(row)
