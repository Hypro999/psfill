from os.path import exists
from settings import CREDENTIALS_FILE, STATIONS_FILE
from typing import Any, Dict, List, Set, Tuple

def load_user_credentials() -> Tuple[str, str, Set[str]]:
    print("Loading user credentials... ", end="", flush=True)

    if not exists(CREDENTIALS_FILE):
        print("Failure.\nCredentials file ({}) not found.".format(CREDENTIALS_FILE))
        exit(1)
    
    data = []  # Sort of like a variable declaration
    with open(CREDENTIALS_FILE, "r") as f:
        data = f.readlines()

    txtemail = ""
    txtpass = ""
    acco = set()  # type: Set[str] 
    for i, line in enumerate(data, start=1):
        try:
            key, value = tuple(map(lambda x: x.strip(), line.split(":", maxsplit=1)))  # I'm sorry ':)
            if key == "username":
                txtemail = value
            elif key == "password":
                txtpass = value
            elif key == "acco":
                acco = set(map(lambda x: x.strip(), value.split(",")))  # likewise ':)
            else:
                print("Failure.\n\"{}\" is an unrecognized key.".format(key))
                exit(1)
        except ValueError:
            # Skip lines which are purely whitespace.
            line = line.strip()
            if line != "":
                print("Failure.\nLine number {} in {} is invalid:\n{}".format(i, CREDENTIALS_FILE, line))
                exit(1)

    if txtemail == "":
        print("Failure.\nUsername was not provided.")
        exit(1)
        
    if txtpass == "":
        print("Failure.\nPassword was not provided.")
        exit(1)

    print("Success.")
    return (txtemail, txtpass, acco)

def load_user_station_preferences(stations_data: Dict[str, Any]) -> List[str]:
    """ This method will also validate the user station preferences. """
    print("Loading user station preferences... ", end="", flush=True)

    if not exists(STATIONS_FILE):
        print("Failure.\nStations Preferences file ({}) not found.".format(STATIONS_FILE))
        exit(1)
   
    user_station_preferences = []  # type: List[str]
    with open(STATIONS_FILE, "r") as f:
        user_station_preferences = f.readlines()

    # Some lines might be a random mixture of whitespace so we can't
    # do verification short-circuiting by analyzing the length of
    # user_station_preferences.

    stations_seen = {}  # type: Dict[str, int]  # [name, line_number]
    validated_user_station_preferences = []
    for i, station in enumerate(user_station_preferences, start=1):
        station = station.strip()
        if station == "":
            continue  # This is how we filter out blank lines.
        if station not in stations_data:
            print("Failed.\nStation \"{}\" on line {} of {} is not a valid station.".format(station, i, STATIONS_FILE))
            exit(1)
        if station in stations_seen:
            print("Failed.\nStation \"{}\" was originally on line {} of {} but was repeated on line {}.".format(station, stations_seen[station], STATIONS_FILE, i))
            exit(1)
        stations_seen[station] = i
        validated_user_station_preferences.append(station)

    if len(validated_user_station_preferences) != len(stations_data):
        print("Failed.\nStations that you have to add to {}:\n{}".format(STATIONS_FILE, set(stations_data) - set(validated_user_station_preferences)))
        exit(1)

    print("Success.")
    return validated_user_station_preferences

