import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.datamad0819 

locations = db.locations.find()
data = pd.DataFrame(locations)
data = data.drop("_id", axis=1)
locations = data.rename(columns={"lat":"Latitude","long":"Longitude"})

def getCoords(lat,long):
    coords = []
    for x,y in zip(lat,long):
        coords.append((x,y))
    return coords

coordinates = getCoords(locations["Latitude"],locations["Longitude"])

def getCompaniesNear(lat,long, max_meters=1000):
    x = list(db.locations.find({
        "position": {
            "$near": {
               "$geometry": {
                  "type": "Point" ,
                  "coordinates": [ long , lat ]
               },
               "$maxDistance": max_meters
             }
       }
    }))
    return ((lat,long),len(x))

list_coords = []
for x in coordinates:
    y = getCompaniesNear(x[0],x[1])
    list_coords.append(y)

def sort_by_count(arr):
    return sorted(arr,key=lambda x: x[1],reverse=True)
list_coords_final = sort_by_count(list_coords)

def getCompanies(lat,long, max_meters=1000):
    return list(db.locations.find({
        "position": {
            "$near": {
               "$geometry": {
                  "type": "Point" ,
                  "coordinates": [ long , lat ]
               },
               "$maxDistance": max_meters
             }
       }
    }))

final_location = getCompanies(*x)
final_location = pd.DataFrame(final_location)
final_location = final_location.drop("_id", axis=1)
final_location = final_location.rename(columns={"lat":"Latitude","long":"Longitude"})
final_location.to_json('../data/final_location.json', orient="records")
