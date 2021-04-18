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

def get_websites(sd):
    params = {"q": sd[0], "textDecorations": True, "textFormat": "HTML"}
    try:
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        jval = json.JSONDecoder().decode(json.dumps(search_results))
        try:
            res = jval['webPages']['value'][0]['url']
        except (KeyError, ValueError):
            res = "JSON ERROR " + sd[0]
        return res, sd[1], sd[2], sd[3]
    except requests.exceptions.RequestException as e:
        print("REQUESTS FAILURE: " + sd[0])
        print(e)
        return "REQUESTS FAILURE " + sd[0], sd[1], sd[2], sd[3]

if __name__ == "__main__":
    libdata = pd.read_excel(config.FILE_PATH)
    temp_libdata = libdata.copy()
    temp_libdata['searchVal'] = temp_libdata['Name'] + " " + temp_libdata['City'] + " " + temp_libdata['State']
    
    searchData = list(temp_libdata[['searchVal', 'Name', 'City', 'State']].itertuples(index=False, name=None))
    #searchData = searchData[:100]
    searchData.append(("fauiwehfgnp;iAOUWENvgjpo;iAJWRhbgahwieuhyfaliUWehfouaw", 'no', 'city', 'here'))
    
    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        list_of_results = list(executor.map(get_websites, searchData))
    t1 = time.perf_counter()

    res_df = pd.DataFrame(list_of_results, columns=['website', 'Name', 'City', 'State'])
    new_libdata = pd.merge(libdata, res_df, how='left', on=['Name', 'City', 'State'])
    
    new_libdata.to_excel(config.TARGET_FILE_PATH)

    print("time: ")
    print(t1-t0)
