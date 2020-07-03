import json
from os.path import exists
from requests import Session
from settings import STATIONS_FILE, url
from time import time
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

def get_pb_token() -> int:
    """
        Based on the JS function:
        $(document).ready(function () {
            var yourDate = new Date();  // for example
            var epochTicks = 621355968000000000;
            var ticksPerMillisecond = 10000;
            var token = epochTicks + (yourDate.getTime() * ticksPerMillisecond);

            getPBdetail($("#Batch option:selected").val(), token)
            $("#Batch").change(function () {
                getPBdetail($(this).val(), token)
            });

            $(".StudentView").click(function () {
                debugger;
                var Id = $(this).attr("StationId");
                getPBdetailPOPUP(Id);
            });
        });
    """
    milliseconds = time() * 1000
    return int(621355968000000000 + 10000 * milliseconds)

def fetch_problem_banks_data(session: Session) -> Dict[str, Any]:
    """
        Use the "problem bank" to fetch detailed data for whatever stations that data exists for.
        This method will return a mapping from the station's ID to the detailed problem bank data
        for that station.
    """
    pb_token = get_pb_token()  # Not sure if this needs to be accurate. But let's keep it accurate anyways...
    payload = {
        "batchid": "undefined",
        "token": str(pb_token),
    }
    response = session.post(url("/Student/ViewActiveStationProblemBankData.aspx/getPBdetail"), json=payload)
    if not response.status_code == 200:
        print("Failed.\n Could not get problem bank information.")
        exit(1)
    raw_data = json.loads(response.json()["d"])

    data = {}  # Dict[str, Any]
    for station in raw_data:
        data[station["StationId"]] = station

    return data

def fetch_detailed_stations_list(session: Session) -> List[Dict[str, Any]]:
    stations_list = get_stations_list(session)
    print("Fetching and adding detailed data to the stations list... ", end="", flush=True)
    incomplete_detailed_stations_data = fetch_problem_banks_data(session)  # Incomplete because of the PSD.

    complete_detailed_stations_list = []
    for station in stations_list:
        station_id = station["StationId"]
        if station_id in incomplete_detailed_stations_data:
            company_data = incomplete_detailed_stations_data[station_id]
            complete_detailed_stations_list.append({
                "CompanyName": company_data["CompanyName"],
                "Tags": company_data["Tags"],
                "stipend": company_data["stipend"],
                "IndustryDomain": company_data["IndustryDomain"],
                "City": company_data["City"],
            })
        else:
            # Heuristic: All of the companies not in the problem bank
            # follow the order "{Industry}-{Name}, {City}" so let's
            # just parse based on the assumption that this property
            # will continue to hold. We will extract this in a not
            # so efficient way but one that's easy to write. We can
            # always improve this part of the code later.
            name = station["Companyname"]
            parts = name.split("-")
            industry_domain = parts[0]  # Don't strip because when we put it all back together again, we need to maintain the bad formatting.
            name = "-".join(parts[1:])
            parts = name.split(",")
            city = parts[-1].strip()  # We need to strip here though or we'll get one extra space.
            company_name = ",".join(parts[:-1]).strip()

            complete_detailed_stations_list.append({
                "CompanyName": company_name,
                "Tags": "-",  # This is already a tag that they use.
                "stipend": 0,
                "IndustryDomain": industry_domain,
                "City": city,
            })

    print("Success.")
    return complete_detailed_stations_list

