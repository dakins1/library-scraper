import concurrent.futures
import re
import pandas as pd
import requests
import config
import json
from bs4 import BeautifulSoup

HREF_TEXT= set(("contact us"))

def get_hrefs(html):
    hrefs = set()
    soup = BeautifulSoup(html, 'html5lib')
    for anchor in soup.find_all("a"):
        if ("href" in anchor.attrs) & (anchor.text.lower().trim() in HREF_TEXT):
            link = anchor.attrs["href"]
            # print("text: " + anchor.text)
            print(anchor.text.lower())
            print("link: " + link)
            hrefs.add(anchor.text)
    return hrefs

def get_contact_us(html):
    hrefs = get_hrefs(html)

def parse_email_from_text(text):
    return set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+[\.com|\.org|\.gov]", text, re.I))
    
def get_html_from_link(ws):
    try: 
        response = requests.get(ws)
        response.raise_for_status()
        return { "success" :True, "html" : response.text, "error": None}
    except requests.exceptions.RequestException as e:
        print("REQUESTS FAILURE: " + ws)
        print(e)
        return {'success': False, "html" : None, "error": e }
    
def get_email_at_all_costs(ws):
    response = get_html_from_link(ws)
    # print("response print: " + json.dumps(response))
    if (response["success"]):
        emails = parse_email_from_text(response["html"])
        if (len(emails) != 0): return emails
        else:
            hrefs = get_contact_us(response["html"])
            return hrefs
    else: return "website invalid " + response["error"]


if __name__ == "__main__":
    libdata = pd.read_excel(config.NEW_FILE_PATH)
    temp_libdata = libdata.copy()
    websites = list(temp_libdata['website'].head())
    wsDemoWithEmail = "https://dallaslibrary2.org/contacts.php"
    wsDemoWithoutEmail = "https://dallaslibrary2.org"
    res = get_email_at_all_costs(wsDemoWithoutEmail)
    print(res)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    #    list_of_results = list(executor.map(get_email, websites))
    # print(list_of_results)
    