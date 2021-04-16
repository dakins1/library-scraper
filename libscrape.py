import json
import time
from collections import deque
import requests
import pandas as pd
import config
#from bs4 import BeautifulSoup
#from urllib.parse import urlsplit
#import re

libdata = pd.read_excel("file:///mnt/c/Users/Dillon/comp/UnitedStatesPublicLibrariesContactInfo-ChildrensProgramming.xlsx")
libdata['searchVals'] = libdata['Name'] + " " + libdata['City'] + " " + libdata['State']
searchVals = libdata['searchVals'].tolist()
searchVals = searchVals[:10]
searchVals.append("fauiwehfgnp;iAOUWENvgjpo;iAJWRhbgahwieuhyfaliUWehfouaw")

SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY}

web_list = deque([])
failures = deque([])

t0 = time.perf_counter()
for sv in searchVals:
    params = {"q": sv, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    jval = json.JSONDecoder().decode(json.dumps(search_results))
    try:
        web_list.append(jval['webPages']['value'][0]['url'])
    except (KeyError, ValueError):
        failures.append(sv)
t1=time.perf_counter()
size = len(web_list)
print("size")
print(size)
print("time")
print(t1-t0)
print("failures")
print(failures)



