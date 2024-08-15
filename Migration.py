from logging.handlers import RotatingFileHandler
from requests.auth import HTTPBasicAuth
from datetime import datetime as dt
from pprint import pprint
import configparser
import requests
import logging
import ast

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config = configparser.ConfigParser()
config.read('creds.ini')
jira_username = config['jira']['jira_user']
jira_token = config['jira']['jira_token']
jira_url = config['jira']['jira_url']
jira_api = config['jira']['rest_api']
asana_api_project = config['asana']['rest_api_projectlevel']
asana_api_section = config['asana']['rest_api_sectionlevel']
asana_api_task = config['asana']['rest_api_tasklevel']
asana_token = config['asana']['access_token']
asana_project_names = ast.literal_eval(config['asana']['asana_project_names'])

jira_auth = HTTPBasicAuth(jira_username, jira_token)
jira_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

asana_headers = {
    "Authorization": f"Bearer {asana_token}",
    "Content-Type": "application/json"
}

jira_params = {
    "maxResults" : 100
}

def jira_initiative(projectgid):
    fields = f'customfield_10090, customfield_10091'
    jql = f'project=STR and issuetype = Initiative and "Asana ID[Short text]" ~ "{projectgid}"'
    url = f'{jira_url}{jira_api}search?jql={jql}&fields={fields}'
    try:
        request = requests.get(url=url, auth=jira_auth, headers=jira_headers)
        response = request.json()
        key = response['issues'][0]['key']
        AsanaID = response['issues'][0]['fields']['customfield_10090']
        AsanaSubObj = response['issues'][0]['fields']['customfield_10091']
        jira_epic_data = jira_epics(key, AsanaID, AsanaSubObj)
        asana_sections_data = asana_sections(AsanaID)
        epics_check(jira_epic_data, asana_sections_data, key, AsanaSubObj)
        jira_story_data = jira_stories(jira_epic_data)
        asana_task_data = tasks_per_epic(key, AsanaID, AsanaSubObj)
        story_check(jira_story_data, asana_task_data)
        logging.info(f'Initiative extracted successfully from jira for {projectgid}')
    except Exception as e:
        logging.error(f'Error in extracting the Initiative data from jira for {projectgid}')

def jira_epics(parentkey, AsanaID, AsanaSubObj):
    issue = []
    fields = f'customfield_10090, customfield_10091'
    jql = f'project=STR and issuetype = Epic and "Asana Sub-Objective[Short text]" ~ "{AsanaSubObj}" AND parent = {parentkey}'
    url = f'{jira_url}{jira_api}search?jql={jql}&fields={fields}'
    try:
        request = requests.get(url=url, auth=jira_auth, headers=jira_headers, params= jira_params )
        response = request.json()
        if response['total'] != 0:
            for issues in response['issues']:
                issue.append({
                    "key" : issues['key'],
                    "AsanaID" : issues['fields']['customfield_10090'],
                    "AsanaSubObj" : issues['fields']['customfield_10091']
                })
        logging.info(f'Epics extracted successfully from jira for {AsanaSubObj}')
        return issue
    except Exception as e:
        logging.error(f'Error in extracting the epics data from jira for {AsanaSubObj}')
        return None

def asana_sections(projectgid):
    url = f'{asana_api_project}{projectgid}/sections?limit=100'
    sections=[]
    try:
        request = requests.get(url=url, headers=asana_headers)
        response = request.json()
        for data in response['data']:
            if data['name'] == 'Untitled section':
                data_check = asana_tasks(data['gid'])
                if data_check != []:
                    sections.append({
                        "name" : data['name'],
                        "gid" : data['gid']
                    })
            else:
                sections.append({
                    "name" : data['name'],
                    "gid" : data['gid']
                })

        logging.info(f'extracted sections from asana for project gid {projectgid}')
        return sections
    except Exception as e:
        logging.error(f'error in getting sections for asana project gid{projectgid}')
        return None
    

def asana_tasks(sectiongid):
     url = f'{asana_api_section}{sectiongid}/tasks?limit=100'
     tasks=[]
     try:
        request = requests.get(url=url, headers=asana_headers)
        response = request.json()
        data = response['data']
        for task in data:
            tasks.append(task)
        logging.info(f'extracted tasks from asana for section gid {sectiongid}')
        return tasks
     except Exception as e:
        logging.error(f'error in getting tasks for asana section gid {sectiongid}')
        return None


def epics_check(jiradata, asanadata, key, AsanaSubObj):
    epic = []
    for x in asanadata:
        gid = x['gid']
        name = x['name']
        present = False
        for y in jiradata:
            if str(y['AsanaID']) == gid:
                present = True
                break
        if present:
            print(f'gid value {gid} is present in jira')
        else:
            epic.append(create_issue("Epic" ,name, gid, AsanaSubObj, key))
    return epic


def create_issue(issuetype ,summary, asanaid, asanasubobj, parent):
    url = f'{jira_url}{jira_api}issue'
    issue_data = {
        "fields": {
            "project": {"key": 'STR'},
            "summary": summary,
            "issuetype": {"name": issuetype},
            "customfield_10090": asanaid,
            "customfield_10091": asanasubobj,
            "parent": {"key": parent}
        }
    }
    response = requests.post(url=url, auth=jira_auth, headers=jira_headers, json=issue_data)
    if response.status_code == 201:
        key = response.json().get('key')
        logging.info(f'Created issue {key} in under {parent}.')
        return key
    else:
        logging.error(f'Failed to create issue: {response.status_code}, {response.text}')
        return None

def jira_stories(data):
    issue = []
    for epic in data:
        epickey = epic['key']
        AsanaSubObj = epic['AsanaSubObj']
        AsanaID = epic['AsanaID']     
        fields = f'customfield_10090, customfield_10091'
        jql = f'project=STR and issuetype = Story and "Asana Sub-Objective[Short text]" ~ "{AsanaSubObj}" AND parent = {epickey}'
        url = f'{jira_url}{jira_api}search?jql={jql}&fields={fields}'
        try:
            request = requests.get(url=url, auth=jira_auth, headers=jira_headers, params= jira_params )
            response = request.json()
            if response['total'] != 0:
                for issues in response['issues']:
                    issue.append({
                        "key" : issues['key'],
                        "AsanaID" : issues['fields']['customfield_10090'],
                        "AsanaSubObj" : issues['fields']['customfield_10091'],
                        "epickey" : epickey,
                        "epicgid" : AsanaID
                    })
            logging.info(f'Stories extracted successfully from jira for {AsanaID}')
        except Exception as e:
            logging.error(f'Error in extracting the Stories data from jira for {AsanaSubObj}')
            return None
    return issue

def tasks_per_epic(key, AsanaID, AsanaSubObj):
    data = jira_epics(key, AsanaID, AsanaSubObj)
    tasks =[]
    for epic in data:
        epic_key = epic['key']
        epic_AsanaID = epic['AsanaID']
        epic_subobj = epic['AsanaSubObj']
        task_data = asana_tasks(epic_AsanaID)
        for task in task_data:
            tasks.append({
                'name': task['name'],
                'gid': task['gid'],
                'subobj' : epic_subobj,
                'epic_key' : epic_key

            })
    return tasks


def story_check(jiradata, asanadata):
    story =[]
    for x in asanadata:
        gid = x['gid']
        name = x['name']
        subobj = x['subobj']
        epic_key = x['epic_key']
        present = False
        for y in jiradata:
            jira_key = y['key']
            if str(y['AsanaID']) == gid:
                present =True
                break
        if present == True:
            logging.info(f'issue already present under parent of {epic_key} with key {jira_key}')
        else:
            story.append(create_issue("Story", name, gid, subobj, epic_key))
    return story






def main():
    for project in asana_project_names:
        jira_initiative(project)


if __name__ == "__main__":
    main()
