# for getting the dataframe to make this project dynamic
#just for testing

import json
import pandas as pd

with open("data/sample_candidates.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.json_normalize(data, sep="_")

print("\nTOTAL COLUMNS:", len(df.columns))
print("\n")

for col in sorted(df.columns):
    print(col)