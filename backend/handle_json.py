import json
import os
import pandas as pd
Base_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

df = pd.read_csv(Base_dir+"/aurin/aurin_vic/income.csv",encoding = 'utf-8',header = 0,index_col=0)



def get_city_income():
    median_aud_2013_14 = df.at["Melbourne (C)","median_aud_2013_14"]
    median_aud_2014_15 = df.at["Melbourne (C)","median_aud_2014_15"]
    return int(median_aud_2013_14),int(median_aud_2014_15)


# with open(Base_dir+"/aurin/aurin_vic/income.csv") as f:
#     line = f.readline()
#     while line != "":
#         line = line.split(",")
#         if line[0] == "Melbourne (C)":
#             median_aud_2013_14 = line[1]
#             median_aud_2014_15 = line[2]
#             break;
#         line = f.readline()




def get_total_count(city):
    if city == 'Melbourne (3000)':
        with open("tweet3.json") as f1:
            total_count = len(f1.readlines())
            return total_count



with open("geo.json",encoding='utf-8',) as f2:
    # city = 'melbourne'
    raw_data = json.load(f2)
    for feature in raw_data['features']:
        if feature['properties']['name'] == 'Melbourne (3000)':
            feature['properties']['tweets_count'] = get_total_count('Melbourne (3000)')
            feature['properties']['income_2013'], feature['properties']['income_2014'] = get_city_income()

    with open('geo_1.json', 'w') as r:
        print (raw_data)
        json.dump(raw_data, r)

    r.close()

f2.close()


