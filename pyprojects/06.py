import requests
import csv

# Jira credentials and base URL
username = "fayaz"
password = "123456789"
jira_url = "http://jira.tafzs.com:8080"

# JQL query to retrieve issues
jql_query = 'project in ("External Legal Project") AND "Customer company name" in ("Angular Directions") AND worklogDate >= startOfMonth(-1M) AND worklogDate <= endOfMonth(-1M) AND worklogAuthor in (fayaz, navi, likitha)'

# API endpoint to retrieve issues
api_url = f"{jira_url}/rest/api/2/search"

# Parameters for the API request
params = {
    "jql": jql_query,
    "maxResults": 1000,  # increase this value to retrieve more issues
    "fields": "worklog,issuetype"
}

# Perform the API request
response = requests.get(api_url, auth=(username, password), params=params)

# Check if the request was successful
if response.status_code == 200:
    # Retrieve the issues from the response JSON
    issues = response.json()["issues"]

    # Print the total number of issues
    print(f"Total number of issues: {len(issues)}")

    # Write the issues and their worklogs and request types to a CSV file
    with open("issues.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Issue key", "Request type", "Log-Date", "Author", "Description", "Time Spent", "Tax"])
        for issue in issues:
            for worklog in issue['fields']['worklog']['worklogs']:
                key = issue["key"]
                request_type = issue["fields"]["issuetype"]["name"]
                LogDate = worklog["started"]
                author = worklog["author"]["name"]
                desc = worklog["comment"]
                timespnt = worklog["timeSpentSeconds"]/360
                comment_parts = desc.split(":")
                valuetaxx = comment_parts[2].strip()
                writer.writerow([key, request_type, LogDate, author, desc, timespnt, valuetaxx])
else:
    print("Error: could not retrieve issues")
