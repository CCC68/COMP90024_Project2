import json
import os
import pandas as pd



df = pd.read_csv("aurin/aurin_nsw/income.csv", encoding='utf-8')
print(130)
# for i in range(131):
#     df.at[i, 'lga_name'] = df.at[i, 'lga_name'].lower()
#
# df.to_csv("aurin/aurin_nsw/income.csv", encoding='utf-8',index=False)