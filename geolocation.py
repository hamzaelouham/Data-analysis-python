from time import sleep
import requests
import pandas as pd
#
Api_key = 'e4c0417954484b158a98533e2bfde4ce'
'''

def getGeoloction(city):
    res = requests.get(f'https://api.opencagedata.com/geocode/v1/json?q=Moabit%2C%20{city}&key={Api_key}&language=fr&pretty=1').json()
    data = res.get('results')
    lat = data[0]['bounds']['northeast']['lat']
    lng = data[0]['bounds']['northeast']['lng']
    print(lat,lng)

getGeoloction('Rabat')

'''


def getDataSets(arg):
    return pd.read_excel(arg)
    


datasets = getDataSets('datasets.xls')    


for i, row in datasets.iterrows():
    city = str(datasets.at[i,'City'])
    sleep(1)
    print(f'requested...{i}')
    res = requests.get(f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={Api_key}&language=fr&pretty=1').json()
    d = res.get('results')
    datasets.at[i,'Lat'] = d[0]['bounds']['northeast']['lat']
    datasets.at[i,'Lng'] = d[0]['bounds']['northeast']['lng']

print('done !')
datasets.to_csv('NewDataSets.csv')