import requests
import json
from datetime import datetime
import discord
def getUserdata(data):
    result = {}

    result['best_rank'] = 1000000000
    result['worst_rank'] = -1000000000
    result['maxRating'] = 0
    result['minRating'] = 1000000000
    result['maxUp'] = 0
    result['maxDown'] = 0
    result['best_contest'] = ''
    result['worst_contest'] = ''
    result['maxUp_contest'] = ''
    result['maxDown_contest'] = ''
    result['rating_graph']=[]

    length = len(data)
    # print(length)
    for i in range (length):
        # print(i)
        contest = data[i]
        result['maxRating'] = max(result['maxRating'], contest['newRating'])
        result['minRating'] = min(result['minRating'], contest['newRating'])

        if (contest['rank'] < result['best_rank']):
            result['best_rank'] = contest['rank']
            result['best_contest'] = contest['contestId']

        if (contest['rank'] > result['worst_rank']):
            result['worst_rank'] = contest['rank'];
            result['worst_contest'] = contest['contestId'];

        ch = contest['newRating'] - contest['oldRating']

        if contest['oldRating'] == 0:
            ch = contest['newRating']-1500
        if (ch > result['maxUp']):
            result['maxUp'] = ch
            result['maxUp_contest'] = contest['contestId']

        if (ch < result['maxDown']):
            result['maxDown'] = ch
            result['maxDown_contest'] = contest['contestId']

        if (i == len(data[0]) - 1):
            result['rating'] = contest['newRating']

        #convert epoch time to human readable
        #ratingUpdateTimeSeconds was given in epoch time so first convert it to
        #human readable
        epoch_time = contest['ratingUpdateTimeSeconds']
        datetime_time = datetime.fromtimestamp(epoch_time)
        # datetime_time = datetime_time.strftime('%Y-%m-%d')
        # print(datetime_time)
        result['rating_graph'].append([datetime_time, contest['newRating']])


    return result

def embedThemAll(user1):
    #this list will save embed as well as rating data which will be retrieved later
    #for plotting graph
    embed_and_rating = []
    handle1 = "https://codeforces.com/api/user.info?handles=" + user1 + ';'
    #retrieve data
    # print(handle1)
    data1 = requests.get(handle1)
    json_obj1 = json.loads(data1.text)
    json_res1 = json_obj1['result'][0]
    img1 = json_res1['titlePhoto']
    img1 = "http:" + img1
    avatar = "http:" + json_res1['avatar']
    #variables
    if 'firstName' in json_res1:
        name = json_res1['firstName'] + " " + json_res1['lastName']
    else:
        name = 'NULL'
    rating = json_res1['rating']
    max_rating = json_res1['maxRating']
    rank = json_res1['rank']
    max_rank = json_res1['maxRank']
    if 'organization' in json_res1:
        org = json_res1['organization']
    else:
        org = 'NULL'

    #retrieve user rating data from api
    api_url = "https://codeforces.com/api/"
    user_rating_data = api_url + 'user.rating?handle=' + user1

    resp1 = requests.get(user_rating_data)
    json_rating1 = json.loads(resp1.text)
    json_rating1 = json_rating1['result']

    #get user data from the above function
    #embed is used to send data in beautiful format to descord
    datastats = getUserdata(json_rating1)
    embed = discord.Embed(title="@"+user1, url=img1,description="These are stats of "+user1, color=0x09b0ce, inline = True)
    embed.set_author(name=name,url=img1)
    embed.set_thumbnail(url=avatar)
    embed.set_image(url=img1)
    embed.add_field(name="Organization", value=org, inline=False)
    embed.add_field(name="Rating", value=rating, inline=True)
    embed.add_field(name="Max-Rating", value=max_rating, inline=False)
    embed.add_field(name="Min-Rating", value=datastats['minRating'], inline=True)
    embed.add_field(name="Rank", value=rank, inline=False)
    embed.add_field(name="Max-Rank", value=max_rank, inline=True)
    embed.add_field(name="Best-Rank", value=datastats['best_rank'], inline=False)
    embed.add_field(name="Worst-Rank", value=datastats['worst_rank'], inline=True)
    embed.add_field(name="Max-Up", value=datastats['maxUp'], inline=False)
    embed.add_field(name="Max-Down", value=datastats['maxDown'], inline=True)
    embed.add_field(name="Best-contest", value=datastats['best_contest'], inline=False)
    embed.add_field(name="Worst-contest", value=datastats['worst_contest'], inline=True)
    embed.add_field(name="MaxUp-contest", value=datastats['maxUp_contest'], inline=False)
    embed.add_field(name="MaxDown-contest", value=datastats['maxDown_contest'], inline=True)
    embed_and_rating.append(embed)
    embed_and_rating.append(datastats['rating_graph'])

    return embed_and_rating
