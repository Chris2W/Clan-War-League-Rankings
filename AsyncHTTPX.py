import requests
import asyncio
import config
import httpx
import decimal
import pandas as pd
import time


headers = {
    'Accept': 'application/json',
    'authorization': f'Bearer {config.TOKEN}'
}
rounds = {
      "rounds": [
    {
      "warTags": [
        "#2C2Y82V2G",
        "#2C2Y882J8",
        "#2C2Y880YU",
        "#2C2Y88G9G"
      ]
    },
    {
      "warTags": [
        "#2C2Q0V20L",
        "#2C2Q0V8PJ",
        "#2C2Q0V9R0",
        "#2C2Q0VL9G"
      ]
    },
    {
      "warTags": [
        "#2C2RUPJ2U",
        "#2C2RUPCL8",
        "#2C2RUYLG8",
        "#2C2RUPUJL"
      ]
    },
    {
      "warTags": [
        "#2C2V2VUYP",
        "#2C2V8200J",
        "#2C2V800VU",
        "#2C2V80PUJ"
      ]
    },
    {
      "warTags": [
        "#2C882VGVP",
        "#2C882VCQU",
        "#2C882VJ9G",
        "#2C882VUU8"
      ]
    },
    {
      "warTags": [
        "#2C8YPYJ8L",
        "#2C8YPYUC0",
        "#2C8YPYCLJ",
        "#2C8YPL02P"
      ]
    },
    {
      "warTags": [
        "#2C8GY0890",
        "#2C8GY09QP",
        "#2C8GY0PCG",
        "#2C8GY2R2G"
      ]
    }
    ]
}

async def get_cwlinfo_from_war_tag():
    response = requests.get('https://api.clashofclans.com/v1/clans/%232Y00GGVCU/currentwar/leaguegroup',headers=headers)
    war_tag_json = response.json()
    # print(war_tag_json['rounds'])
    my_dict = {}
    for item in rounds['rounds']:
        warTags_list = item['warTags']
        for war_tag in warTags_list:
            war_tag = war_tag[1:]
            # print(war_tag) #excludes hashtag
            #war tag changes in http url with a 23 in front of the tag

            #HTTPX ASYNC
            async with httpx.AsyncClient() as client: 
                cwl_response = await client.get(f'https://api.clashofclans.com/v1/clanwarleagues/wars/%23{war_tag}', headers=headers)
                cwl_json = cwl_response.json()
                # print(cwl_json)

                #when we are not the opponent as described in api
                if cwl_json['clan']['tag'] == "#2Y00GGVCU": 
                    # print(cwl_json['clan']['members'])
                    for member in cwl_json['clan']['members']:
                        if 'attacks' in member:
                            enemy = member['attacks'][0]['defenderTag']
                            for i in range(len(cwl_json['opponent']['members'])):
                                if cwl_json['opponent']['members'][i]['tag'] == enemy:
                                    # needs adjusting later
                                    if cwl_json['opponent']['members'][i]['mapPosition'] > 30 and member['mapPosition'] <= 30:
                                        adjust = cwl_json['opponent']['members'][i]['mapPosition'] - 30
                                        diff = abs(member['mapPosition']-adjust)
                                        my_dict[member['name']] = my_dict.get(member['name'],0) + diff
                                        
                                    elif member['mapPosition'] > 30 and cwl_json['opponent']['members'][i]['mapPosition'] <= 30:
                                        memberAdjust = member['mapPosition'] - 30
                                        diff = abs(memberAdjust-cwl_json['opponent']['members'][i]['mapPosition'])
                                        my_dict[member['name']] = my_dict.get(member['name'],0) + diff
                                        
                                    else:
                                        diff = abs(member['mapPosition']-cwl_json['opponent']['members'][i]['mapPosition'])
                                        my_dict[member['name']] = my_dict.get(member['name'],0) + diff
                                        
                                else: continue
                
                #if we are considered an opponent in api
                elif cwl_json['clan']['tag'] != "2Y00GGVCU" and cwl_json['opponent']['tag'] == '#2Y00GGVCU':
                    for member in cwl_json['opponent']['members']:
                        if 'attacks' in member:
                            enemy = member['attacks'][0]['defenderTag']
                            for i in range(len(cwl_json['clan']['members'])):
                                if cwl_json['clan']['members'][i]['tag'] == enemy:
                                    #neends adjusting later
                                    if cwl_json['clan']['members'][i]['mapPosition'] > 30 and member['mapPosition'] <= 30:
                                        adjust = cwl_json['clan']['members'][i]['mapPosition'] - 30
                                        diff = abs(member['mapPosition']-adjust)
                                        my_dict[member['name']] = my_dict.get(member['name'],0) + diff
                                        
                                    elif member['mapPosition'] > 30 and cwl_json['clan']['members'][i]['mapPosition'] <= 30:
                                        memberAdjust = member['mapPosition'] - 30
                                        diff = abs(memberAdjust-cwl_json['clan']['members'][i]['mapPosition'])
                                        
                                        my_dict[member['name']] = my_dict.get(member['name'],0) + diff

                                    else:
                                        diff = abs(member['mapPosition']-cwl_json['clan']['members'][i]['mapPosition'])
                                        my_dict[member['name']] = my_dict.get(member['name'],0) + diff
                                        
                                else: continue   
                # print(cwl_json['opponent']['members'])
    # print(my_dict)
    for key,val in my_dict.items():
        val = round(decimal.Decimal(val) / decimal.Decimal(len(rounds['rounds'])),3)
        my_dict[key] = float(val)
    
    res = sorted(my_dict.items(), key = lambda x: x[0])
    return res
    #less is better

async def get_avg_stars_from_players():
    response = requests.get('https://api.clashofclans.com/v1/clans/%232Y00GGVCU/currentwar/leaguegroup',headers=headers)
    war_tag_json = response.json()
    # print(war_tag_json['rounds'])
    my_dict = {}
    for item in rounds['rounds']:
        warTags_list = item['warTags']
        for war_tag in warTags_list:
            war_tag = war_tag[1:]
            # print(war_tag) #excludes hashtag
            #war tag changes in http url with a 23 in front of the tag
            async with httpx.AsyncClient() as client: 
                cwl_response = await client.get(f'https://api.clashofclans.com/v1/clanwarleagues/wars/%23{war_tag}', headers=headers)
                cwl_json = cwl_response.json()
                # print(cwl_json)

                #when we are not the opponent as described in api (when we're the MCS)
                if cwl_json['clan']['tag'] == "#2Y00GGVCU": 
                    # print(cwl_json['clan']['members'])
                    for member in cwl_json['clan']['members']:
                        if 'attacks' in member:
                            my_dict[member['name']] = my_dict.get(member['name'],0) + member['attacks'][0]['stars']
                
                #if we are considered an opponent in api
                elif cwl_json['clan']['tag'] != "2Y00GGVCU" and cwl_json['opponent']['tag'] == '#2Y00GGVCU':
                    for member in cwl_json['opponent']['members']:
                        if 'attacks' in member:
                            my_dict[member['name']] = my_dict.get(member['name'],0) + member['attacks'][0]['stars']
    # print(my_dict)

    for key,val in my_dict.items():
        val = round(decimal.Decimal(val) / decimal.Decimal(len(rounds['rounds'])),2)
        my_dict[key] = float(val)
    
    res = sorted(my_dict.items(), key = lambda x: x[0])
    return res
    
def tester():
    war_tag = "2C8GY2R2G"
    yuh = rounds['rounds'][len(rounds)-1]['warTags']
    war_tag2 = rounds['rounds'][len(rounds)-1]['warTags'][len(yuh)-1][1:]
    print(war_tag2)
    cwl_response = requests.get(f'https://api.clashofclans.com/v1/clanwarleagues/wars/%23{war_tag}', headers=headers)
    cwl_json = cwl_response.json()
    if cwl_json['clan']['tag'] == "#2Y00GGVCU": 
        print(cwl_json['clan']['members'])

async def get_ratio_of_attacks():
    response = requests.get('https://api.clashofclans.com/v1/clans/%232Y00GGVCU/currentwar/leaguegroup',headers=headers)
    war_tag_json = response.json()
    # print(war_tag_json['rounds'])
    my_dict = {}
    for item in rounds['rounds']:
        warTags_list = item['warTags']
        for war_tag in warTags_list:
            war_tag = war_tag[1:]

            async with httpx.AsyncClient() as client: 
                cwl_response = await client.get(f'https://api.clashofclans.com/v1/clanwarleagues/wars/%23{war_tag}', headers=headers)
                cwl_json = cwl_response.json()

                #when we are not the opponent as described in api
                if cwl_json['clan']['tag'] == "#2Y00GGVCU": 
                    # print(cwl_json['clan']['members'])
                    for member in cwl_json['clan']['members']:
                        if 'attacks' in member:
                            my_dict[member['name']] = my_dict.get(member['name'],0) + 1
                
                #if we are considered an opponent in api
                elif cwl_json['clan']['tag'] != "2Y00GGVCU" and cwl_json['opponent']['tag'] == '#2Y00GGVCU':
                    for member in cwl_json['opponent']['members']:
                        if 'attacks' in member:
                            my_dict[member['name']] = my_dict.get(member['name'],0) + 1
    return sorted(my_dict.items(), key = lambda x: x[0])

#tester()
def combine():
    first_list = asyncio.run(get_cwlinfo_from_war_tag())
    second_list = asyncio.run(get_avg_stars_from_players())
    third_list = asyncio.run(get_ratio_of_attacks())
    new_list = []

    for distance,stars,attackRatio in zip(first_list,second_list,third_list):
        new_list.append((distance[0],distance[1],stars[1],f"{attackRatio[1]}/{len(rounds['rounds'])}",round(attackRatio[1]/len(rounds['rounds']),2)))

    return new_list

#name, avg stars, avg distance of position
    # for i in new_list:
    #     print(i)

# combine()
#get_ratio_of_attacks()
start_time = time.time()
data = combine()

df = pd.DataFrame(data, columns=['Name','mapPosDiff','avgStars','strWarAttacks','warAttackRatio'])
df.sort_values(['mapPosDiff', 'avgStars', 'warAttackRatio'], ascending=[True, False, False], inplace=True)
df['overall_rank'] = 1
df['overall_rank'] = df.groupby(['warAttackRatio'])['overall_rank'].cumsum()

df.to_csv('CWL_Rankings.csv', encoding='utf-8', index=False)
print(f"HTTPX: {time.time() - start_time} seconds")