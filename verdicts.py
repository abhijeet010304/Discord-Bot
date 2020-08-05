import requests
import json
# import discord
#get verdict and other data I have retrieved much data which can be used to
# expand the bot further
def verdict(user1):
    api_url = "https://codeforces.com/api/"
    user_status_data = api_url + 'user.status?handle=' + user1

    response = requests.get(user_status_data)
    json_status1 = json.loads(response.text)
    json_status1 = json_status1['result']
    data = json_status1
    problems = {}
    verdicts = {}
    language = {}
    tags = {}
    levels = {}
    length = len(data)
    alldata = []
    # print(length)
    # print(data[0])
    for i in range(length - 1, -1, -1):
        status = data[i]
        # print(status)
        if 'contestId' in status['problem']:
            problemId = str(status['problem']['contestId']) + '-' + str(status['problem']['index'])
        else:
            problemId = "Misc"
        if problemId in problems:
            if problems[problemId]['solved'] == 0:
                problems[problemId]['attempts'] += 1
        else:
            problems[problemId] = {"attempts": 1, 'solved': 0}

        if status['programmingLanguage'] in language:
            language[status['programmingLanguage']] += 1
        else:
            language[status['programmingLanguage']] = 1

        if status['problem']['index'] in levels:
            levels[status['problem']['index']] += 1
        else:
            levels[status['problem']['index']] = 1

        if status['verdict'] in verdicts:
            verdicts[status['verdict']] += 1
        else:
            verdicts[status['verdict']] = 1

        if status['verdict'] == 'OK':
            problems[problemId]['solved'] += 1
        #be careful about the type of data stored in api
        if problems[problemId]['solved'] == 1 and status['verdict'] == 'OK':
            for t in status['problem']['tags']:
                if t in tags:
                    tags[t] += 1
                else:
                    tags[t] = 1

    alldata.append(language)
    alldata.append(levels)
    alldata.append(problems)
    alldata.append(tags)
    alldata.append(verdicts)
    return alldata
