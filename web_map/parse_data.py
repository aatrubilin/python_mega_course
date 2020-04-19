# parsing data from http://opendata.novo-sibirsk.ru
import json

import requests
import pandas as pd
from geopy.geocoders import ArcGIS

arc_gis = ArcGIS()

url = "http://opendata.novo-sibirsk.ru/_layouts/MSTeam.OpenData/Handlers/RibbonHandler.ashx"
params = {
    "id": 65,  # data id
    "type": "GetOpenDataServerSide",
    "page": 1,
    "column": 1,
    "order": "asc",
    "pCount": 1000000,
}

cur_row = 0


def geocode(address):
    global cur_row
    cur_row += 1
    print(f"{cur_row}. {address}...", end="")
    location = arc_gis.geocode(address)
    print(" OK")
    return location


print(f"Request data with params {params}...", end="")
response = requests.get(url, params=params)

if response.ok:
    print(" Response ok")
    print("Parsing data...", end="")
    data = json.loads(response.json()["Args"])
    arr = pd.DataFrame(data["data"])
    arr = arr.drop([0, 7], axis=1)
    arr.columns = ["Type", "District", "Street", "House", "SportType", "Phone"]
    print(f" Parsed {arr.shape[0]} rows")

    print(f"Get locations...")
    arr["Full address"] = "Россия, Новосибирск, " + arr["Street"] + ", " + arr["House"]
    arr["Location"] = arr["Full address"].apply(geocode)
    arr["Latitude"] = arr["Location"].apply(lambda x: x.latitude if x else None)
    arr["Longitude"] = arr["Location"].apply(lambda x: x.longitude if x else None)
    print("Get locations... OK")

    arr = arr.drop(["Full address", "Location"], axis=1)
    print("Saving data...", end="")
    arr.to_csv('nsk_sports.csv', index=False)
    print(" Success")
