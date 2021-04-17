import json
import time
import concurrent.futures 
from collections import deque
import requests
import pandas as pd
import config
#from bs4 import BeautifulSoup
#from urllib.parse import urlsplit
#import re

SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY}

def get_websites(sv):
    params = {"q": sv, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    jval = json.JSONDecoder().decode(json.dumps(search_results))
    try:
        res = jval['webPages']['value'][0]['url']
    except (KeyError, ValueError):
        res = "FAILURE " + sv
    return res

if __name__ == "__main__":
    libdata = pd.read_excel(config.FILE_PATH)
    libdata['searchVals'] = libdata['Name'] + " " + libdata['City'] + " " + libdata['State']
    searchVals = libdata['searchVals'].tolist()
    searchVals = searchVals[:100]
    searchVals.append("fauiwehfgnp;iAOUWENvgjpo;iAJWRhbgahwieuhyfaliUWehfouaw")
    t0 = time.perf_counter()
    #list_of_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        list_of_results = list(executor.map(get_websites, searchVals))
    t1 = time.perf_counter()
    print(list(list_of_results))
    print("time: ")
    print(t1-t0)
