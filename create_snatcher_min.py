#!/usr/bin/env python3
"""creating a minified version of the file to just know legendary, ... common"""
import json
import os.path

PRETTY_FILE = "snatcher_data.json"
MIN_FILE = "snatcher_min.json"

snatchers = {}
if os.path.isfile(PRETTY_FILE):
    with open(PRETTY_FILE) as json_file:
        snatchers = json.load(json_file)

def write_to_file(filename: str, snatchers, indent: int):
    """write file"""
    with open(filename, "w", encoding="utf-8") as snatchers_file:
        json.dump(snatchers, snatchers_file, indent=indent, sort_keys=True)

#print(snatchers)
min_snatchers = {}
for snatcher in snatchers:
    snatcher_data = snatchers[snatcher]
    min_snatcher = {}
    min_snatcher["address"] = snatcher_data["address"]
    min_snatcher["id"] = snatcher_data["id"]
    min_snatcher["title"] = snatcher_data["title"]
    min_snatcher["rank"] = snatcher_data["rank"]
    min_snatcher["score"] = snatcher_data["score"]
    min_snatcher["uri"] = snatcher_data["uri"]

    attributes_to_track = ["background", "beard", "body", "cape", "costume", "eyes", "eyewear", "full_mask", "gun", "haircut", "handheld", "headwear", "mask", "mouth_enhancement", "mouth_special", "skull_enhancement", "special"]
    legendary = 0
    epic = 0
    rare = 0
    uncommon = 0
    common = 0
    LIMIT_LEGENDARY = 1.49
    LIMIT_EPIC = 4.99
    LIMIT_RARE = 14.99
    LIMIT_UNCOMMON = 29.99

    for attribute in attributes_to_track:
        rarity = snatcher_data[attribute]["rarity"]
        if rarity > 0 and rarity <= LIMIT_LEGENDARY:
            legendary+=1
        elif rarity > LIMIT_LEGENDARY and rarity <= LIMIT_EPIC:
            epic+=1
        elif rarity > LIMIT_EPIC and rarity <= LIMIT_RARE:
            rare+=1
        elif 15 > LIMIT_RARE and rarity <= LIMIT_UNCOMMON:
            uncommon+=1
        else:
            common+=1
    min_snatcher["legendary"] = legendary
    min_snatcher["epic"] = epic
    min_snatcher["rare"] = rare
    min_snatcher["uncommon"] = uncommon
    min_snatcher["common"] = common



    min_snatchers[snatcher] = min_snatcher

write_to_file(MIN_FILE, min_snatchers, 0)

