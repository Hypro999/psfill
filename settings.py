from os.path import abspath, dirname, join

ROOT_URL = "http://psd.bits-pilani.ac.in"
BASE_DIR = dirname(abspath(__file__))
STATIONS_FILE = join(BASE_DIR, ".config", "stations.txt")
CREDENTIALS_FILE = join(BASE_DIR, ".config", "credentials.txt")

def url(endpoint: str) -> str:
    return ROOT_URL + endpoint

