#!/usr/bin/env python3
"""scraping page howrare.is to get info about rarity as json file"""
import json
import os.path
import requests
import cloudscraper
from bs4 import BeautifulSoup

from random import randint
from time import sleep

PRETTY_FILE = "snatcher_data.json"
FILE = "snatcher_data_small.json"
SNATCHERS_SIZE = 10020
SAVE_EVERY = 50

def sanetize_key(key: str):
    """remove colon and replace space with underscore"""
    return key.replace("\n", "").strip().lower().replace(":", "").replace(" ", "_")

def sanetize_value(value: str):
    """remove spaces and other info"""
    return value.replace("\n", "").strip().replace("                          ", " ").replace("\n    BUY", "")

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

#snatchers that don't exist => 10001 - 10020 
blacklist = [158, 214, 279, 1142, 1143, 1758, 2785, 3369, 3542, 3759, 4113, 4129, 4149, 4478, 4510, 6265, 6340, 6630, 7136, 7456]
for snatcher in blacklist:
    missing_snatchers.remove(snatcher)

print(missing_snatchers)

count_to_save = 0
for missing_snatcher in missing_snatchers:
    print(missing_snatcher)
    scraper = cloudscraper.create_scraper()
    response = scraper.get("https://howrare.is/solsnatchers/"+str(missing_snatcher)+"/")

    snatcher = {}
    snatcher["id"] = missing_snatcher
    soup = BeautifulSoup(response.content, "html.parser")
    if "CAPTCHA" in soup.getText():
        print("Resolve captcha - Cloudflare")
        print(soup.getText())
        exit()

    stats = soup.find(class_="stats_full")
    if stats is None:
        print("snatcher", missing_snatcher, "not found")
        sleep(randint(0,2))
        continue

    for div in stats.find_all('div'):
        if "rank" in div.text:
            snatcher["rank"] = float(sanetize_value(div.find('span').text))
        if "score" in div.text:
            snatcher["score"] = float(sanetize_value(div.find('span').text))
        if "attribute count" in div.text:
            snatcher["attribute_count"] = float(sanetize_value(div.find('span').text))
    
    title = soup.find(class_="overflow")
    snatcher["title"] = sanetize_value(title.find('span').text.strip())
    address = sanetize_value(title.find('a').attrs["href"])
    snatcher["address"] = sanetize_value(address[address.rindex("/")+1:])

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
            snatcher[key] = details
        else:
            snatcher[key] = value
    
    img = soup.find(class_="nfts_detail_img")
    href = img.find("a")
    snatcher["uri"] = sanetize_value(href.attrs["href"])
    snatchers[str(missing_snatcher)] = snatcher

    sleep(randint(0,2))

    count_to_save+=1
    if count_to_save >= SAVE_EVERY:
        write_to_file(PRETTY_FILE, snatchers, 4)
        write_to_file(FILE, snatchers, 0)
        count_to_save = 0
        print("saving")
    

write_to_file(PRETTY_FILE, snatchers, 4)
write_to_file(FILE, snatchers, 0)
print("done")

