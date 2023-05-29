import requests
import csv
import re
import pandas as pd
from github import Github

jira_url = 'http://jira.tafzs.com:8080/rest/api/2'
username = 'fayaz'
password = '123456789'

jql_query = 'project in ("External Legal Project") AND "Customer company name" in ("Angular Directions") AND worklogDate >= startOfMonth(-1M) AND worklogDate <= endOfMonth(-1M) AND worklogAuthor in (fayaz, navi, likitha)'

headers = {
    'Accept': 'application/json'
}
auth = (username, password)

issues = requests.get(jira_url + '/search', params={'jql': jql_query}, headers=headers, auth=auth).json()['issues']

fieldnames = ['Issue Key', 'Request Type', 'Author', 'Time Spent', 'Start Time', 'Comment', 'Amount', 'Tax',
              'Total Amount']

# users_hourly_rate
hourly_rate_for_fayaz = 200
hourly_rate_for_likitha = 150
hourly_rate_for_Navi = 100

with open('jiraworklogdata.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames)

    writer.writeheader()

for issue in issues:
    issue_key = issue['key']
    request_type = issue['fields']['issuetype']['name']
    worklogs = requests.get(jira_url + '/issue/' + issue_key + '/worklog', headers=headers, auth=auth).json()[
        'worklogs']
    sorted_worklogs = sorted(worklogs, key=lambda x: x['started'])

    valueamount = 0
    valuetax = 0
    TotalAmount = 0

    for worklog in sorted_worklogs:
        comment = worklog['comment']
        name = worklog['author']['name']
        if 'EXCLUDE' not in comment:
            pattern = r"^(Fixed|fixed|FIXED):(\d+):(\d+):(.*)$"
            match = re.match(pattern, comment)
            if match:
                word, value1, value2, comment_text = match.groups()
                valueamount = int(value1)
                valuetax = int(value2)

            elif 'fayaz' in name:
                time_spent = worklog['timeSpentSeconds'] / 60  # Convert to minutes
                cost = time_spent * (hourly_rate_for_fayaz / 60)  # Calculate cost for this worklog
                valueamount = cost
                valuetax = 10
            elif 'likitha' in name:
                time_spent = worklog['timeSpentSeconds'] / 60  # Convert to minutes
                cost = time_spent * (hourly_rate_for_likitha / 60)  # Calculate cost for this worklog
                valueamount = cost
                valuetax = 10
            elif 'navi' in name:
                time_spent = worklog['timeSpentSeconds'] / 60  # Convert to minutes
                cost = time_spent * (hourly_rate_for_Navi / 60)  # Calculate cost for this worklog
                valueamount = cost
                valuetax = 10
            percentage_amount = valueamount * (valuetax / 100)
            TotalAmount = valueamount + percentage_amount

            with open('jiraworklogdata.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    issue_key,
                    request_type,
                    worklog['author']['name'],
                    worklog['timeSpent'],
                    worklog['started'],
                    worklog['comment'],
                    valueamount,
                    valuetax,
                    TotalAmount,

                ])

df = pd.read_csv('jiraworklogdata.csv')
df2 = df._append((pd.DataFrame(df['Total Amount'].sum(), index=["Total"], columns=["Total Amount"])))
df2.to_csv('jiraworklogdata.csv', index=False)

g = Github("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")
repo = g.get_repo("KoushikVardhan/worklogdata")
with open("jiraworklogdata.csv", "r") as file:
    content = file.read()
repo.create_file("KoushikVardhan/worklogdata.csv", "Successful", content)


