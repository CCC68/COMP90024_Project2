import json
import os
import pandas as pd
import urllib.request

Base_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

# resceive the backend request of state
state = 'vic'
# aurin city income list
df_income = pd.read_csv(Base_dir+f"/aurin/aurin_{state}/income.csv", encoding='utf-8')
df_obesity = pd.read_csv(Base_dir+f"/aurin/aurin_{state}/obesity.csv", encoding='utf-8')
df_population = pd.read_csv(Base_dir+f"/aurin/aurin_{state}/population.csv", encoding='utf-8')
# shift to lower case
city_list = df_income['lga_name'].tolist()



def get_record(url):
    resp = urllib.request.urlopen(url)
    ele_json = json.loads(resp.read())
    return ele_json

def get_city_income(city):

    median_aud_2014_15 = df_income.loc[df_income['lga_name'] == city, "median_aud_2014_15"]
    return int(median_aud_2014_15)

def get_city_obesity(city):

    median_aud_2014_15 = df_obesity.loc[df_obesity['lga_name'] == city, "ovrwgt_p_1_count"]
    return int(median_aud_2014_15)

def get_city_population(city):

    median_aud_2014_15 = df_population.loc[df_population['lga_name'] == city, "erp_2016pr"]
    return int(median_aud_2014_15)

def get_total_count(city, map_json):

    tweet_count = 0
    for each in map_json['rows']:
        if each['key'].lower().find(city) != -1:
            tweet_count += each['value']
    return tweet_count


with open(Base_dir+f'/aurin/{state}.json',encoding='utf-8',) as f2:
    url = f'http://172.26.132.118:5984/bitcoin_{state}_db/_design/bitcoint_location_count/_view/all?group=true'

    #raw_data 是原始的geo.json
    raw_data = json.load(f2)

    # data1 是mapreduce回来的key-value对(twitter result)
    data1 = get_record(url)

    for city in city_list:

        for feature in raw_data['features']:
            if (feature['properties']["vic_lga__3"]).lower() == city:
                feature['properties']['tweets_count'] = get_total_count(city, data1)
                feature['properties']['income_2014'] = get_city_income(city)
                feature['properties']['obesity_rate'] = get_city_obesity(city)
                feature['properties']['population'] = get_city_population(city)

    #所有城市遍历完再写进去
    with open(Base_dir+f'/aurin/{state}_plus.json', 'w') as r:
        print(raw_data)
        json.dump(raw_data, r)

    r.close()

f2.close()