from argparse import ArgumentParser
from lib.auth import authenticate
from lib.auto_order import hypergen
from lib.fetch import fetch_stations_data, generate_default_stations_file
from lib.post import send_station_preferences
from lib.user import load_user_credentials, load_user_station_preferences
from requests import Session

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-g","--generate", help = "generate new default station list.", action = "store_true")
    parser.add_argument("-y","--yes", help = "when used with -g it means that the stations file should be overwritten if exists (don't prompt).", action = "store_true")
    parser.add_argument("--hypergen", help = "generate new station list using hypergen.", action = "store_true")
    args = parser.parse_args()
    session = Session()
    txtemail, txtpass, acco = load_user_credentials()
    authenticate(session, txtemail, txtpass)
    if args.hypergen:
        hypergen(session)
    elif args.generate:
        generate_default_stations_file(session, args.yes)
    else:
        stations_data = fetch_stations_data(session)
        user_station_preferences = load_user_station_preferences(stations_data)
        send_station_preferences(session, stations_data, user_station_preferences, acco)

