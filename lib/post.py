import json
from os.path import exists
from requests import Session
from settings import STATIONS_FILE, url
from typing import Any, Dict, List, Set

def send_station_preferences(session: Session, stations_data: Dict[str, Any], user_station_preferences: List[str], acco: Set[str]) -> None:
    print("Sending station preferences... ", end="", flush=True)
    jsondata = []
    for i, station in enumerate(user_station_preferences, start=1):
        station_data = stations_data[station]
        jsondata.append({
            "isActive": "1",  # All of them are. Why is this a string anyways?
            "PreferenceNo": str(i),  # Yes, this also needs to be a string. 
            "StationId": station_data["station_id"],
            "Accommodation": str(station_data["city"] in acco).lower(),  # This shouldn't be a string either!
        }) # I didn't design this silly API, I'm just using it.
    payload = {
        "jsondata": json.dumps(jsondata),
        "jsonvalue": "",  # Random useless parameter
        "contistation": "0"  # likewise?
    }
    response = session.post(url("/Student/StudentStationPreference.aspx/saveStudentStationPref"), json=payload)
    if response.status_code != 200:
        print("Failed")
        exit(1)
    try:
        message = json.loads(response.json()["d"])[0]["message"]
        if message != "Station Preference Submitted Successfully.":
            print(message)
            exit(1)
        print("Success.")
    except:
        print("Failed.")
        exit(1)

    return

