import requests
import csv
import re
import pandas as pd

jira_url = 'https://xit-link.com/rest/api/2'
username = 'hbf98'
password = 'AngularIcecream_123!'

jql_query = 'project = "Angular Legal Service Desk" AND issue in (ALSD-53, ALSD-54, ALSD-55,ALSD-57, ALSD-58)'

headers = {
    'Accept': 'application/json'
}
auth = (username, password)

issues = requests.get(jira_url + '/search', params={'jql': jql_query}, headers=headers, auth=auth).json()['issues']
print(issues)
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
            pattern = r"^(.*):(\d+):(\d+):(.*)$"
            match = re.match(pattern, comment)
            if match:
                word, value1, value2, comment_text = match.groups()
                valueamount = int(value1)
                valuetax = int(value2)

            elif 'fayaz test' in name:
                time_spent = worklog['timeSpentSeconds'] / 60  # Convert to minutes
                cost = time_spent * (hourly_rate_for_fayaz / 60)  # Calculate cost for this worklog
                valueamount = cost
                valuetax = 10
            elif 'fayazclient' in name:
                time_spent = worklog['timeSpentSeconds'] / 60  # Convert to minutes
                cost = time_spent * (hourly_rate_for_likitha / 60)  # Calculate cost for this worklog
                valueamount = cost
                valuetax = 10
            elif 'agent user' in name:
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
