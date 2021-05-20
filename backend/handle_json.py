import json
import os
import pandas as pd
import urllib.request

Base_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

df = pd.read_csv(Base_dir+"/aurin/aurin_vic/income.csv", encoding='utf-8', header=0, index_col=0)
city_list = df.index.tolist()



def get_record(url):
    resp = urllib.request.urlopen(url)
    ele_json = json.loads(resp.read())
    return ele_json

def get_city_income(city):
    if city not in city_list:
        return 0, 0

    median_aud_2013_14 = df.at[city, "median_aud_2013_14"]
    median_aud_2014_15 = df.at[city, "median_aud_2014_15"]

    return int(median_aud_2013_14), int(median_aud_2014_15)


# with open(Base_dir+"/aurin/aurin_vic/income.csv") as f:
#     line = f.readline()
#     while line != "":
#         line = line.split(",")
#         if line[0] == "Melbourne (C)":
#             median_aud_2013_14 = line[1]
#             median_aud_2014_15 = line[2]
#             break;
#         line = f.readline()


#placeholder for map_json
file=""

def get_total_count(city ,map_json):
    tweet_count = 0
    for each in map_json:
        if each['key'].find(city) != -1:
            tweet_count += each['value']
            return tweet_count



with open("geo.json",encoding='utf-8',) as f2:
    url = 'http://82.156.182.19:5984/bitcoindb/_design/bitcoint_location_count/_view/all?group=true'

    #raw_data 是原始的geo.json
    raw_data = json.load(f2)

    # data1 是mapreduce回来的key-value对
    data1 = get_record(url)

    #
    for city in city_list:

        for feature in raw_data['features']:
            if feature['properties']['name'] == city:
                feature['properties']['tweets_count'] = get_total_count(city,data1)
                feature['properties']['income_2013'], feature['properties']['income_2014'] = get_city_income(city)

    #所有城市遍历完再写进去
    with open('geo_1.json', 'w') as r:
        print (raw_data)
        json.dump(raw_data, r)

    r.close()

f2.close()

