import pandas as pd

df1=pd.read_csv("data/goalscorers.csv",encoding="utf-8")
df2=pd.read_csv("data/results.csv",encoding="utf-8")

print("Shape1:",df1.shape)
print("Shape2:",df2.shape)

print("\nColmuns1:",df1.columns.to_list())
print("\nColmuns2:",df2.columns.to_list())

print("\nFirst 5 rows for df1:")
print(df1.head())

print("\nFirst 5 rows for df2:")
print(df2.head())

print("\ndf1 types:")
print(df1.dtypes)

print("\ndf2 types:")
print(df2.dtypes)

print("\nMissing data1:")
print(df1.isnull().sum())

print("\nMissing data2:")
print(df2.isnull().sum())

#======= CLEANING ========

#df1 cleaned

df1.rename(columns={"team":"Winner Team"},inplace=True)
df1_clean=df1.drop(columns=["minute"])
df1_clean["Date"]=pd.to_datetime(df1_clean["date"])
before1=len(df1_clean)
df1_clean=df1_clean.drop_duplicates()
after1=len(df1_clean)
print(f"Dublicates1 removed: {before1-after1}") 

#df2 cleaned

df2_clean=df2.dropna(subset=["home_score","away_score"]).copy()
df2_clean["Date"]=pd.to_datetime(df2_clean["date"])
before2=len(df2_clean)
df2_clean=df2_clean.drop_duplicates()
after2=len(df2_clean)
print(f"Dublicates2 removed: {before2-after2}")

print("\nNew Shape1:",df1_clean.shape)
print("New Shape2:",df2_clean.shape)

import requests
import json
# ====== API SOURCE ======
API_KEY="64dea145dd8e48d098f9e6b563d9f83b"
url = f"https://api.football-data.org/v4/matches"
response=requests.get(url,headers={"X-Auth-Token":API_KEY})
data=response.json()
with open("data/api_response.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
print("✅ API response saved!")
#convert to dataframe
Matches=data["matches"]
df_api=pd.DataFrame(Matches)
print("API Sample")
print(df_api.head())
print("\nShape_API:",df_api.shape)

#==== MERGE ====
df_combined=pd.concat([df1_clean,df2_clean,df_api],ignore_index=True)
print("\nCombined Shape:",df_combined.shape)
print("\nCombined Sample:")
print(df_combined.head())

#saved data
df_combined.to_csv("data/combined_data_football.csv",index=False)
print("\nCombined file saved!")
