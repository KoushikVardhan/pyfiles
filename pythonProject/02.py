import re
import csv


comment =worklog['comment']
# Define regular expression to extract integers
pattern = r"(\w+):(\d+):(\d+):(\w+)"
pattern1 = r"(\w+):(\d+):(\d+)"
pattern2 = r"(\w+):(\d+):(\w+)"
pattern3 = r"(\w+):(\d+)"

# Extract integer values using regular expression
match = re.search(pattern, comment)
match1 = re.search(pattern1, comment)
match2 = re.search(pattern2, comment)
match3 = re.search(pattern3, comment)
if match:
    valueamount = int(match.group(2))
    valuetax = int(match.group(3))
elif match1:
    valueamount = int(match1.group(2))
    valuetax = int(match1.group(3))
elif match2:
    valueamount = int(match2.group(2))
elif match3:
    valueamount = int(match3.group(2))
else:
    valueamount = 0,
    valuetax = 0

