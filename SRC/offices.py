from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017/")
db = client.datamad0819 

query = {"$and":[{"total_money_raised": {"$regex" : "[BM]" }},{"total_money_raised": {"$regex" : "[€$]" }},
                 {"$or":[{"category_code":"software"},{"category_code":"web"},
                     {"category_code":"mobile"},{"category_code":"games_video"},
                     {"category_code":"advertising"},{"category_code":"design"},
                     {"category_code":"photo_video"},{"category_code":"ecommerce"}]}]}

project = {"_id":0, "name":1,"offices.city":1,"offices.latitude":1,"offices.longitude":1,"category_code":1}

companies = db.companies.find(query,project)
data = pd.DataFrame(companies)

def findOffices(df):
    names = []
    category_codes = []
    cities = []
    lats = []
    longs = []
    for name,category_code,office in zip(df["name"],df["category_code"],df["offices"]):
        if len(office) >0:
            for x in range(len(office)):
                names.append(name)
                category_codes.append(category_code)
                cities.append(office[x]['city'])
                lats.append(office[x]['latitude'])
                longs.append(office[x]['longitude'])
    
    dict_companies = {"name":names,"category_code":category_codes,"city":cities,"lat":lats,"long":longs}
    return pd.DataFrame(dict_companies)

data_companies = findOffices(data)

def createGeoJson(office):
    return {
        "type":"Point",
        "coordinates":[office["long"],office["lat"]]
    }


data_companies['position'] = data_companies.apply(createGeoJson, axis=1)
data_companies = data_companies.dropna()

def drop_less_10( df, column):
    keys = df[column].value_counts().index
    values = df[column].value_counts().values
    countries = {keys[i]: values[i] for i in range(len(keys))}
    drop_countries = []

    for i in countries:
        if countries[i] < 10:
            drop_countries.append(i)
        else:
            pass
 
    for c in drop_countries:
        df = df[df[column] != c]

    return df

data_companies = drop_less_10(data_companies,"city")

data_companies = data_companies[data_companies["city"] != '']

data_companies.to_json('../data/offices.json', orient="records")

print("Input this on terminal: mongoimport --db datamad0819 --collection offices --jsonArray ../data/offices.json")