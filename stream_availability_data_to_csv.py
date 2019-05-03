import csv
import json
import time

import requests

# The URL provided by oslobysykkel.no
STATION_STATUS_URL = "https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"

# Slightly less than 10 seconds just to be sure
WAIT_INTERVAL = 9
CHECK_INTERVAL = 0.2

# Order in which the keys should appear in the output CSV
KEY_ORDER = [
    'timestamp',
    'station_id',
    'is_installed',
    'is_renting',
    'is_returning',
    'last_reported',
    'num_bikes_available',
    'num_docks_available',
]


def stations_iter(payload):
    timestamp = payload['last_updated']
    stations = payload['data']['stations']
    for station in stations:
        yield {
            'timestamp': timestamp,
            **station,
        }


def file_is_empty(file):
    file.seek(0)
    if file.read(1):
        file.seek(0)
        return False
    return True


def get_csv_writer(file):
    writer = csv.DictWriter(file, KEY_ORDER)
    if file_is_empty(file):
        writer.writeheader()
    return writer


def convert_to_csv_rows(response, output_filename):
    payload = json.loads(response)
    with open(output_filename, "a+", newline="") as file:
        writer = get_csv_writer(file)
        for station in stations_iter(payload):
            writer.writerow(station)


def repeat_periodically(func, args=(), interval=WAIT_INTERVAL, check_interval=CHECK_INTERVAL):
    previous_time = time.time()
    while True:
        if time.time() - previous_time > interval:
            func(*args)
            previous_time = time.time()
        time.sleep(check_interval)


def add_newest_results_to_csv(client_identifier, output_filename):
    result = requests.get(
        STATION_STATUS_URL,
        headers={
            "Client-Identifier": client_identifier,
        }
    )
    convert_to_csv_rows(result.content.decode("utf-8"), output_filename)


def add_results_to_csv_forever(*args):
    repeat_periodically(add_newest_results_to_csv, args, WAIT_INTERVAL)


def main():
    client_identifier = input("Client-Identifier: ")
    output_filename = input("Output CSV file: ")
    print("Writing to {}.".format(output_filename))
    add_results_to_csv_forever(client_identifier, output_filename)

if __name__ == "__main__":
    main()
