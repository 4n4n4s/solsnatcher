#!/usr/bin/env python3
"""scraping page howrare.is to get info about rarity as json file"""
import json
import os.path
import requests
import cloudscraper
from bs4 import BeautifulSoup

PRETTY_FILE = "snatcher_data.json"
FILE = "snatcher_data_small.json"
SNATCHERS_SIZE = 10000
SAVE_EVERY = 50

def sanetize_key(key: str):
    """remove colon and replace space with underscore"""
    return key.strip().lower().replace(":", "").replace(" ", "_")

def sanetize_value(value: str):
    """remove spaces and other info"""
    return value.strip().replace("                          ", " ").replace("\n    BUY", "")

def write_to_file(filename: str, snatchers, indent: int):
    """write file"""
    with open(filename, "w", encoding="utf-8") as snatchers_file:
        json.dump(snatchers, snatchers_file, indent=indent, sort_keys=True)

snatchers = {}
if os.path.isfile(PRETTY_FILE):
    with open(PRETTY_FILE) as json_file:
        snatchers = json.load(json_file)

missing_snatchers = list(range(1, SNATCHERS_SIZE+1))

for snatcher in snatchers:
    missing_snatchers.remove(int(snatcher))

print(missing_snatchers)

count_to_save = 0
for missing_snatcher in missing_snatchers:
    print(missing_snatcher)
    scraper = cloudscraper.create_scraper()
    response = scraper.get("https://howrare.is/solsnatchers/"+str(missing_snatcher)+"/")

    snatcher = {}
    soup = BeautifulSoup(response.content, "html.parser")
    if "CAPTCHA" in soup.getText():
        print("Resolve captcha - Cloudflare")
        print(soup.getText())
        exit()
    results = soup.find(class_="attributes")
    
    if results != None:
        children = results.findChildren("li", recursive = False)
        for child in children:
            key = sanetize_key(child.findChildren("span", recursive = False)[0].getText())
            value = sanetize_value(child.findChildren("div", recursive = False)[0].getText())
            if value.find('%') > 0:
                
                details = {}
                details["item"] = value[0:value.rfind('(')].strip()
                rarity = value[value.rfind('(')+1:value.index('%')].strip()
                details["rarity"] = float(rarity)
                snatcher[key] = details
            else:
                snatcher[key] = value
        snatchers[str(missing_snatcher)] = snatcher
    else:
        print("can't get info for", missing_snatcher)

    count_to_save+=1
    if count_to_save >= SAVE_EVERY:
        write_to_file(PRETTY_FILE, snatchers, 4)
        write_to_file(FILE, snatchers, 0)
        count_to_save = 0
        print("saving")
    

write_to_file(PRETTY_FILE, snatchers, 4)
write_to_file(FILE, snatchers, 0)
print("done")

