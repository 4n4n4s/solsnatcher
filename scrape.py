#!/usr/bin/env python3
"""scraping page howrare.is to get info about rarity as json file"""
import json
import os.path
import requests
import cloudscraper
from bs4 import BeautifulSoup

from random import randint
from time import sleep

# CONFIGURE THESE PROPERTIES

# COLLECTION = "solsnatchers"
COLLECTION = "solsnatchers_hellhounds"

# COLLECTION_SIZE = 10100 #solsnatchers
COLLECTION_SIZE = 3500

#BLACKLIST = [158, 214, 279, 1142, 1143, 1758, 2785, 3369, 3542, 3759, 4113, 4129, 4149, 4478, 4510, 6265, 6340, 6630, 7136, 7456] #solsnatchers
BLACKLIST = [186, 527, 700, 928, 1271, 1327, 1391, 1679, 1910, 1948, 2949, 3488, 3489, 3490, 3491, 3492, 3493, 3494, 3495, 3496, 3497, 3498, 3499, 3500]

# SAVE TO FILE INTERVAL AFTER EVERY X ITEMS
SAVE_EVERY = 50
# CONFIGURATION END

URL= "https://howrare.is/{}".format(COLLECTION) + "/{}/"
PRETTY_FILE = "{}_data.json".format(COLLECTION)
FILE = "{}_data_small.json".format(COLLECTION)

def sanetize_key(key: str):
    """remove colon and replace space with underscore"""
    return key.replace("\n", "").strip().lower().replace(":", "").replace(" ", "_")

def sanetize_value(value: str):
    """remove spaces and other info"""
    return value.replace("\n", "").strip().replace("                          ", " ").replace("\n    BUY", "")

def write_to_file(filename: str, collection_entries, indent: int):
    """write file"""
    with open(filename, "w", encoding="utf-8") as collection_file:
        json.dump(collection_entries, collection_file, indent=indent, sort_keys=True)

collection_entries = {}
if os.path.isfile(PRETTY_FILE):
    with open(PRETTY_FILE) as json_file:
        collection_entries = json.load(json_file)

print("loaded {} from file".format(len(collection_entries)))
missing_collection_entries = list(range(0, COLLECTION_SIZE+1))


for collection_entry in collection_entries:
    missing_collection_entries.remove(int(collection_entry))


for collection_entry in BLACKLIST:
    missing_collection_entries.remove(collection_entry)

print(missing_collection_entries)

count_to_save = 0
for missing_collection_entry in missing_collection_entries:
    print(missing_collection_entry)
    scraper = cloudscraper.create_scraper()
    url = URL.format(str(missing_collection_entry))
    response = scraper.get(url)

    collection_entry = {}
    collection_entry["id"] = missing_collection_entry
    soup = BeautifulSoup(response.content, "html.parser")
    if "CAPTCHA" in soup.getText():
        print("Resolve captcha - Cloudflare")
        print(soup.getText())
        exit()

    stats = soup.find(class_="stats_full")
    if stats is None:
        print("{} {} not found at {}".format(COLLECTION, missing_collection_entry, url))
        sleep(randint(0,2))
        continue

    for div in stats.find_all('div'):
        if "rank" in div.text:
            collection_entry["rank"] = int(sanetize_value(div.find('span').text))
        if "score" in div.text:
            collection_entry["score"] = int(sanetize_value(div.find('span').text))
        if "attribute count" in div.text:
            collection_entry["attribute_count"] = int(sanetize_value(div.find('span').text))
    
    title = soup.find(class_="overflow")
    collection_entry["title"] = sanetize_value(title.find('span').text.strip())
    address = sanetize_value(title.find('a').attrs["href"])
    collection_entry["address"] = sanetize_value(address[address.rindex("/")+1:])

    attributes = soup.find(class_="attributes")
    for div in attributes.find_all(class_='attribute'):
        value = div.find('span').text.strip()
        text = div.text.strip()
        key = sanetize_key(div.contents[0])
        value = sanetize_value(value)
        percentage = div.contents[2]
        if percentage.find('%') > 0:
            rarity = percentage[percentage.rfind('(')+1:percentage.index('%')].strip()
            details = {}
            details["item"] = value
            details["rarity"] = float(rarity)
            collection_entry[key] = details
        else:
            collection_entry[key] = value
    
    img = soup.find(class_="nfts_detail_img")
    href = img.find("a")
    collection_entry["uri"] = sanetize_value(href.attrs["href"])
    collection_entries[str(missing_collection_entry)] = collection_entry

    sleep(randint(0,2))

    count_to_save+=1
    if count_to_save >= SAVE_EVERY:
        write_to_file(PRETTY_FILE, collection_entries, 4)
        write_to_file(FILE, collection_entries, 0)
        count_to_save = 0
        print("saving")
    

write_to_file(PRETTY_FILE, collection_entries, 4)
write_to_file(FILE, collection_entries, 0)
print("done")

