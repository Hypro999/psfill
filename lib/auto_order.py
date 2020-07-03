import json
import functools
from lib.fetch import fetch_detailed_stations_list
from lib.user import load_user_favorite_stations
from requests import Session
from settings import STATIONS_FILE
from typing import Set

industryDomainRanks = {
    "IT": 1,
    "Finance and Mgmt": 2,
    "Electronics": 3,
    "Others": 4,
    "Health Care": 5,
    "Mechanical": 6,
    "Infrastructure": 7,
    "Chemical": 8,
    "Govt Research Lab": 9,
}

def getTags(x):
    tags = []
    for tag in x["Tags"].split(","):
        tags.append(tag.strip())
    return tags

def industryDomainPriority(x):
    return industryDomainRanks.get(x["IndustryDomain"].strip(), 10)

def csCompatible(x):
    xtags = getTags(x)
    if "A7" in xtags:
        return True
    if "Any" in xtags:
        return True
    if "-" in xtags:
        # This is a weird decision we have to make...
        return True
    return False

def compare(x, y):
    # Step 1: Make sure that it's for CS students.
    xcs = csCompatible(x)
    ycs = csCompatible(y)

    if xcs and not ycs:
        return -1

    if ycs and not xcs:
        return 1

    # Step 2: Look at the industry domain.
    xidp = industryDomainPriority(x)
    yidp = industryDomainPriority(y)
    if xidp < yidp:
        return -1

    if yidp < xidp:
        return 1

    # Step 3: Look at the stipend values.
    if x["stipend"] > y["stipend"]:
        return -1
    if x["stipend"] < y["stipend"]:
        return 1

    return 0

def hypergen(session: Session):
    """
        Automatically create a stations.txt file that will first place my preferred
        stations at the top then sort all of the remaining stations based on:
            1. Eligibility
            2. Industry
            3. Stipend
        This should be applicable to all CS students and with a little tweaking should
        work for all other branches by just modifying the industryDomainRanks map and
        the csCompatible function.
    """
    print("Executing HyperGen...\n\t", end="", flush=True)
    data = fetch_detailed_stations_list(session)
    print("\tSorting data... ", end="", flush=True)
    data.sort(key=functools.cmp_to_key(compare))
    print("Success.")

    print("\t", end="")
    favorite_stations = load_user_favorite_stations()

    print("\tGenerating entries... ", end="", flush=True)
    entries = []
    entries_set = set()  # type: Set[str]
    for station in favorite_stations:
        if station not in entries_set:
            entries_set.add(station)
            entries.append(station)
    for detailed_station in data:
        if detailed_station["IndustryDomain"]:
            entry = "{}-{}, {}".format(detailed_station["IndustryDomain"], detailed_station["CompanyName"], detailed_station["City"])
        else:
            entry = "{}, {}".format(detailed_station["CompanyName"], detailed_station["City"])
        if entry not in entries_set:
            entries_set.add(entry)
            entries.append(entry)
    print("Success.")

    print("\tWriting to stations file... ", end="", flush=True)
    with open(STATIONS_FILE, "w+") as f:
        for entry in entries:
            f.write(entry + "\n")
    print("Success.")

    print("HyperGen ran successfully.")
    return

