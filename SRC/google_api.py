import requests
import os
from dotenv import load_dotenv
load_dotenv()
import base64
import pandas as pd
import time

google_token = os.getenv("google_token")

def locationData(city,myquery):
    names = []
    citys = []
    lats = []
    longs = []
    for cit,quer in zip(city,myquery):
        response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&fields=geometry/location,name&key={}".format(quer,google_token))
        data = response.json()
        time.sleep(20)
        for place in data["results"]:
            names.append(place["name"])
            citys.append(cit)
            lats.append(place["geometry"]["location"]["lat"])
            longs.append(place["geometry"]["location"]["lng"])
    dict_extras = {"name":names,"city":citys,"lat":lats,"long":longs}
    return pd.DataFrame(dict_extras)

def createGeoJson(office):
    return {
        "type":"Point",
        "coordinates":[office["long"],office["lat"]]
    }

cities = ['San Francisco', 'New York City', 'Palo Alto', 
          'London', 'Mountain View', 'Seattle', 'Sunnyvale', 
          'San Mateo', 'Redwood City', 'Los Angeles', 'Boston', 'Austin', 
          'Paris', 'San Jose', 'Santa Clara', 'Cambridge', 'Santa Monica', 
          'Chicago', 'San Diego', 'Menlo Park', 'Berlin']


queries_starbucks = []
for city in cities:
    myquery = "starbucks+"+"in+"+city.replace(" ","")
    queries_starbucks.append(myquery)
data_starbucks = locationData(cities,queries_starbucks)
data_starbucks['position'] = data_starbucks.apply(createGeoJson, axis=1)
data_starbucks["category_code"] = "Starbucks"
data_starbucks = data_starbucks[["name","category_code","city","lat","long","position"]]

queries_burger = []
for city in cities:
    myquery = "burger+restaurant+"+"in+"+city.replace(" ","")
    queries_burger.append(myquery)
data_burger = locationData(cities,queries_burger)
data_burger['position'] = data_burger.apply(createGeoJson, axis=1)
data_burger["category_code"] = "burger"
data_burger = data_burger[["name","category_code","city","lat","long","position"]]

queries_irish = []
for city in cities:
    myquery = "irish+pub+"+"in+"+city.replace(" ","")
    queries_irish.append(myquery)
data_irish = locationData(cities,queries_irish)
data_irish['position'] = data_irish.apply(createGeoJson, axis=1)
data_irish["category_code"] = "pub"
data_irish = data_irish[["name","category_code","city","lat","long","position"]]

queries_nightclub = []
for city in cities:
    myquery = "nightclub+"+"in+"+city.replace(" ","")
    queries_nightclub.append(myquery)
data_nigthclub = locationData(cities,queries_nightclub)
data_nigthclub['position'] = data_nigthclub.apply(createGeoJson, axis=1)
data_nigthclub["category_code"] = "nightclub"
data_nigthclub = data_nigthclub[["name","category_code","city","lat","long","position"]]

queries_mexican = []
for city in cities:
    myquery = "mexican+restaurant+"+"in+"+city.replace(" ","")
    queries_mexican.append(myquery)
data_mexican = locationData(cities,queries_mexican)
data_mexican['position'] = data_mexican.apply(createGeoJson, axis=1)
data_mexican["category_code"] = "mexican"
data_mexican = data_mexican[["name","category_code","city","lat","long","position"]]

queries_comics = []
for city in cities:
    myquery = "comic+book+shop+"+"in+"+city.replace(" ","")
    queries_comics.append(myquery)
data_comics = locationData(cities,queries_comics)
data_comics['position'] = data_comics.apply(createGeoJson, axis=1)
data_comics["category_code"] = "comic book shop"
data_comics = data_comics[["name","category_code","city","lat","long","position"]]

data_extras = pd.concat([data_starbucks,data_burger,data_irish,data_nigthclub,data_mexican,data_comics])

#Join tables to have all locations in one json

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.datamad0819 

project = {"_id":0}

offices = db.offices.find()
data = pd.DataFrame(offices)
data = data.drop("_id", axis=1)

locations = pd.concat([data,data_extras])
locations = locations.rename(columns={"lat":"Latitude","long":"Longitude"})

locations.to_json('../data/locations.json', orient="records")

print("Input this on terminal: mongoimport --db datamad0819 --collection locations --jsonArray ../data/locations.json")