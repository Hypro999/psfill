import json
from os.path import exists
from requests import Session
from settings import STATIONS_FILE, url
from typing import Any, Dict, List

def get_stations_list(session: Session) -> List[Dict[str, Any]]:
    stations_data_endpoint = url("/Student/StudentStationPreference.aspx/getinfoStation")
    response = session.post(stations_data_endpoint, json={"CompanyId": "0"})  # We have to send a POST request to get data.... Ok, seriously, which IDIOT designed this portal?!
    if response.status_code != 200:
        print("Failed.")
        exit(1)
    stations_list = json.loads(response.json()["d"])
    return stations_list

def fetch_stations_data(session: Session) -> Dict[str, Any]:
    print("Loading the currently available stations... ", end="", flush=True)
    get_stations_list(session)
    stations_list = get_stations_list(session)
    stations_data = {}  # type: Dict[str, Any]
    for station in stations_list:
        company_name = station["Companyname"].strip()
        stations_data[company_name] = {
            "sno": station["Sno"],
            "city": station["City"],
            "station_id": station["StationId"],
            "company_id": station["CompanyId"],
        }
    print("Success.")
    return stations_data

def generate_default_stations_file(session: Session, auto_override: bool) -> None:
    output_filename = STATIONS_FILE
    if not auto_override:
        while exists(output_filename):
            opt = "c"
            while opt not in ["y", "n"]:
                opt = input("The file {} already exists. Overwrite (y/n)? ".format(output_filename))
            if opt == "y":
                break
            elif opt == "n":
                output_filename = input("Then what file do you want to write to? ")

    print("Generating the updated PS list... ",end = "", flush = True)
    stations_list = get_stations_list(session)
    company_list = [station["Companyname"].strip() for station in stations_list]
    
    with open(output_filename, "w+") as f:
        for company in company_list: 
            f.write(company + "\n")

    print("Success.")
    return


