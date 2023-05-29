import requests
from requests.auth import HTTPBasicAuth
import json
import configparser
from datetime import datetime, timezone
import sys
import csv
import urllib3

urllib3.disable_warnings()


def get_response(url, headers, auth):
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth,
        verify=False
    )
    return response


def put_response(url, payload, headers, auth):
    response = requests.request(
        "PUT",
        url,
        data=payload,
        headers=headers,
        auth=auth,
        verify=False
    )
    return response


def post_response(url, payload, headers, auth):
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth,
        verify=False
    )
    return response


def main():
    config = configparser.ConfigParser()
    config.read('01.ini')
    server = config['jira']['server_url']
    user = config['jira']['server_user']
    token = config['jira']['server_token']
    rest_api = config['jira']['rest_api']
    query = config['info']['query']
    # fields = config['info']['fields']
    print(server, user, token, rest_api, query)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    auth = HTTPBasicAuth(user, token)
    url = "%s%s%s" % (server, rest_api, query)
    print(url)
    pro_response = get_response(url, headers, auth)
    issuedata = pro_response.json()

    # Extract the total number of issues
    total_issues = issuedata["total"]

    # Print the total number of issues
    print("Total Issues: {}".format(total_issues))


if __name__ == "__main__":
    main()
