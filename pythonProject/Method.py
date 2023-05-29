def amountexceptfixed():
    amount1 = 250,
    amount2 = 200,
    amount3 = 100,
    timespentinmin = worklog['timeSpentSeconds']/60,
    if worklog['author']['name'] == "fayaz":
        valueamount = amount1 * timespentinmin,
    elif worklog['author']['name'] == "likitha":
        valueamount = amount2 * timespentinmin,
    elif worklog ['author']['name'] == "Navi":
        valueamount = amount3 * timespentinmin,
    else:
        valueamount = amount3 * timespentinmin





