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

with open('combinationmethod.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Issue Key', 'Request Type', 'Author', 'Time Spent', 'Start Time', 'Comment'])

for issue in issues:
    issue_key = issue['key']
    request_type = issue['fields']['issuetype']['name']
    worklogs = requests.get(jira_url + '/issue/' + issue_key + '/worklog', headers=headers, auth=auth).json()['worklogs']
    for worklog in worklogs:
        with open('combinationmethod.csv', 'a', newline='') as file:
            def amountexceptfixed():
                amount1 = 250,
                amount2 = 200,
                amount3 = 100,
                #timespentinmin = worklog['timeSpentSeconds']/60,
                if worklog['timeSpent'].endswith("m"):
                    time_minutes = int(worklog['timeSpent'][:-1])
                else:
                    time_minutes = 0

                if worklog['author']['name'] == "fayaz":
                    valueamount1 = amount1 * time_minutes/60,
                elif worklog['author']['name'] == "likitha":
                    valueamount1 = amount2 * time_minutes/60,
                elif worklog['author']['name'] == "Navi":
                    valueamount1 = amount3 * time_minutes/60,
                else:
                    valueamount1 = amount3 * time_minutes
                return valueamount1
            comment = worklog['comment']
            pattern = r"(\w+):(\d+):(\d+):(\w+)"
            # Extract integer values using regular expression
            match = re.search(pattern, comment)
            if match and re.search("FIXED", comment):
                valueamount = int(match.group(2))
                valuetax = int(match.group(3))
            else:
                valuetax = 10,
                valueamount = amountexceptfixed()

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
