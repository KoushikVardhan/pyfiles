

from jira import JIRA
import csv

options = {
    'server': 'http://jira.tafzs.com:8080'
}
jira = JIRA(options, basic_auth=('fayaz', '123456789'))

issues = jira.search_issues('project in ("External Legal Project") AND "Customer company name" in ("Angular Directions") AND worklogDate >= startOfMonth(-1M) AND worklogDate <= endOfMonth(-1M) AND worklogAuthor in (fayaz, navi, likitha)')

with open('worklog2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Issue Key', 'Request Type', 'Log-Date', 'Author', 'comment', 'Tax', 'Time Spent', 'Amount'])

for issue in issues:
    for worklog in jira.worklogs(issue):
        x1 = worklog.author.name,
        x2: tuple[int] = 0,
        x3 = 0,
        if x1 == 'fayaz':
            x2 = 10,
            pass
        elif x1 == 'likitha':
            x2 = 20,
            pass
        elif x1 == 'alok':
            x2 = 30,
            pass
        elif x1 == 'Navi':
            x2 = 5,
            pass
        else:
            x2 = 0,

        with open('worklog2.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                issue.key,
                issue.fields.issuetype.name,
                worklog.created,
                worklog.author.name,
                worklog.comment,
                x2,
                worklog.timeSpentSeconds/3600,

            ])
