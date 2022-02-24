#!/usr/bin/env python3
"""creating a minified version of the file to just know legendary, ... common"""
import json
import os.path


# CONFIGURE THESE PROPERTIES

# COLLECTION = "solsnatchers"
COLLECTION = "solsnatchers_hellhounds"

#ATTRIBUTES_TO_TRACK = ["background", "beard", "body", "cape", "costume", "eyes", "eyewear", "full_mask", "gun", "haircut", "handheld", "headwear", "mask", "mouth_enhancement", "mouth_special", "skull_enhancement", "special"]

ATTRIBUTES_TO_TRACK = ["background", "body", "collar", "eyes", "legs", "mouth_object"]
# CONFIGURATION END

PRETTY_FILE = "{}_data.json".format(COLLECTION)
MIN_FILE = "{}_min.json".format(COLLECTION)

LIMIT_LEGENDARY = 1.49
LIMIT_EPIC = 4.99
LIMIT_RARE = 14.99
LIMIT_UNCOMMON = 29.99

collection = {}
if os.path.isfile(PRETTY_FILE):
    with open(PRETTY_FILE) as json_file:
        collection = json.load(json_file)


def write_to_file(filename: str, collection, indent: int):
    """write file"""
    with open(filename, "w", encoding="utf-8") as collection_file:
        json.dump(collection, collection_file, indent=indent, sort_keys=True)


#print(collection)
minified_collection = {}
for snatcher_entry in collection:
    snatcher_entry_data = collection[snatcher_entry]
    minified_entry = {}
    minified_entry["address"] = snatcher_entry_data["address"]
    minified_entry["id"] = snatcher_entry_data["id"]
    minified_entry["title"] = snatcher_entry_data["title"]
    minified_entry["rank"] = snatcher_entry_data["rank"]
    minified_entry["score"] = snatcher_entry_data["score"]
    minified_entry["uri"] = snatcher_entry_data["uri"]

    legendary = 0
    epic = 0
    rare = 0
    uncommon = 0
    common = 0

    for attribute in ATTRIBUTES_TO_TRACK:
        rarity = snatcher_entry_data[attribute]["rarity"]
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
    minified_entry["legendary"] = legendary
    minified_entry["epic"] = epic
    minified_entry["rare"] = rare
    minified_entry["uncommon"] = uncommon
    minified_entry["common"] = common
    minified_collection[snatcher_entry] = minified_entry


write_to_file(MIN_FILE, minified_collection, 0)
