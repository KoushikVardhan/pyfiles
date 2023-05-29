import requests
import csv
from requests.auth import HTTPBasicAuth

# Jira credentials
jira_username = "fayaz"
jira_password = "123456789"
jira_url = "http://jira.tafzs.com:8080"



# Jira REST API endpoint for retrieving wls
url = f"{jira_url}/rest/api/2/search"

# Authorization header for Jira REST API
auth_header = requests.auth.HTTPBasicAuth(jira_username, jira_password)

# Jira REST API request headers
headers = {"Accept": "application/json"}

# Sending the Jira REST API request to retrieve wls
response = requests.get(url, auth=auth_header, headers=headers)

# Checking if the Jira REST API request was successful
if response.status_code != 200:
    raise Exception(f"Failed to retrieve worklogs for {issue_key}")

# Converting Jira REST API response to JSON format
worklogs = response.json()


# Opening CSV file to write worklogs data
with open("worklogs3.csv", mode="w", newline="") as csv_file:
    fieldnames = ["Issue Key", "Request Type", "Log Date", "Author", "Description", "Hours Spent"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Writing CSV file header row
    writer.writeheader()

    # Looping through worklogs and writing data to CSV file
for issue in worklogs:
    for worklog in worklogs:
        writer.writerow({
            "Issue Key": issue.key,
            "Request Type": worklog["updateAuthor"]["displayName"],
            "Log Date": worklog["created"],
            "Author": worklog["author"]["displayName"],
            "Description": worklog["comment"],
            "Hours Spent": worklog["timeSpentSeconds"] / 3600
        })



