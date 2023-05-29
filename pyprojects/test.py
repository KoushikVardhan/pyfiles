import requests
import json

# Jira Cloud API endpoint URLs
source_url = "https://mcauk.atlassian.net/rest/api/2"
destination_url = "https://catapultcx.atlassian.net/rest/api/2"

# API tokens for authentication
source_token = "ATATT3xFfGF0qwHpVlb8nqF7GJV2GE1lpfEFIBuXunk2UQArq1PnHsW26UbDevidJi-7CecjGhKxxRxvEfDgufvU8WDTbPPur57WaT-N98IfwkUwkdQ2xFiK9I074WCV-Koe1F55vg7aup0v7BqboM9DxHl4dq5I1KYms6tROsUguigwxulxTlM=0663BBC1"
destination_token = "ATATT3xFfGF0qwHpVlb8nqF7GJV2GE1lpfEFIBuXunk2UQArq1PnHsW26UbDevidJi-7CecjGhKxxRxvEfDgufvU8WDTbPPur57WaT-N98IfwkUwkdQ2xFiK9I074WCV-Koe1F55vg7aup0v7BqboM9DxHl4dq5I1KYms6tROsUguigwxulxTlM=0663BBC1"

# Project key and issue types
source_project_key = "BCN"
destination_project_key = "BCN"
issue_types = []  # List of issue types to transfer (optional, empty list means all issues)


# Function to create an issue in the destination Jira Cloud
def create_issue(issue_data):
    url = f"{destination_url}/issue"
    headers = {
        "Authorization": f"Bearer {destination_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(issue_data))
    if response.status_code == 201:
        print("Issue created successfully in the destination Jira Cloud.")
    else:
        print("Failed to create issue in the destination Jira Cloud.")


# Function to transfer issues from the source to the destination Jira Cloud
def transfer_issues():
    # Get all issues from the source Jira Cloud
    url = f"{source_url}/search"
    headers = {
        "Authorization": f"Bearer {source_token}",
        "Content-Type": "application/json"
    }
    data = {
        "jql": f"project = {source_project_key}",
        "fields": "summary,assignee,parent"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        issues = response.json()["issues"]
        for issue in issues:
            issue_data = {
                "fields": {
                    "project": {"key": destination_project_key},
                    "summary": issue["fields"]["summary"],
                    "issuetype": {"name": issue["fields"]["issuetype"]["name"]}
                }
            }
            if "assignee" in issue["fields"]:
                issue_data["fields"]["assignee"] = {"name": issue["fields"]["assignee"]["name"]}
            if "parent" in issue["fields"]:
                issue_data["fields"]["parent"] = {"key": issue["fields"]["parent"]["key"]}
            create_issue(issue_data)
    else:
        print("Failed to retrieve issues from the source Jira Cloud.")


# Transfer the issues
transfer_issues()
