import csv
import requests
from requests.auth import HTTPBasicAuth

# Set up Jira credentials and API endpoint
JIRA_USERNAME = 'fayaz'
JIRA_API_TOKEN = '123456789'
JIRA_API_ENDPOINT = 'http://jira.tafzs.com:8080/rest/api/2/search'

# Set up CSV file path and field names
CSV_FILE_PATH = 'worklog2.csv'
CSV_FIELDNAMES = ['issue_key', 'worklog_id', 'author', 'time_spent_seconds', 'created_at', 'updated_at']

# Set up Jira search parameters to retrieve worklog data
JIRA_SEARCH_PARAMS = {
    'jql': 'project = "project in ("External Legal Project") AND "Customer company name" in ("Angular Directions") '
           'AND worklogDate >= startOfMonth(-1M) AND worklogDate <= endOfMonth(-1M) AND worklogAuthor in (fayaz, '
           'navi, likitha)"',
    'fields': 'key,worklog',
    'maxResults': 1000,
    'startAt': 0
}

# Set up headers for Jira API request
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Set up empty list to store worklog data
worklog_data = []

# Make Jira API requests to retrieve worklog data
while True:
    response = requests.get(
        f'{JIRA_API_ENDPOINT}',
        params=JIRA_SEARCH_PARAMS,
        headers=headers,
        auth=requests.auth.HTTPBasicAuth(JIRA_USERNAME, JIRA_API_TOKEN)
    )

    data = response.json()

    # Add worklog data to list
    for issue in data['issues']:
        for worklog in issue['fields']['worklog']['worklogs']:
            worklog_data.append({
                'issue_key': issue['key'],
                'worklog_id': worklog['id'],
                'author': worklog['author']['displayName'],
                'time_spent_seconds': worklog['timeSpentSeconds'],
                'created_at': worklog['created'],
                'updated_at': worklog['updated']
            })

    # Check if there are more worklogs to retrieve
    if data['startAt'] + len(data['issues']) >= data['total']:
        break
    else:
        JIRA_SEARCH_PARAMS['startAt'] += len(data['issues'])

# Write worklog data to CSV file
with open(CSV_FILE_PATH, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
    writer.writeheader()
    for worklog in worklog_data:
        writer.writerow(worklog)

print(f'{len(worklog_data)} worklogs written to {CSV_FILE_PATH}')
