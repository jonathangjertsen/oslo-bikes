import csv
import json

import requests


STATION_INFO_URL = "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
KEY_ORDER = ['station_id', 'name', 'address', 'lat', 'lon', 'capacity']


def clean_station_data(station):
    station = station.copy()
    for key in ('name', 'address'):
        station[key] = station[key].replace("\n", "")
    return station


def write_station_info(client_identifier, output_filename):
    result = requests.get(
        STATION_INFO_URL,
        headers={
            "Client-Identifier": client_identifier,
        }
    )
    payload = json.loads(result.content.decode("utf-8"))
    with open(output_filename, "w+", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, KEY_ORDER)
        writer.writeheader()
        for station in payload['data']['stations']:
            station = clean_station_data(station)
            writer.writerow(station)


def main():
    client_identifier = input("Client-Identifier: ")
    output_filename = input("Output CSV file: ")

    print("Writing to {}".format(output_filename))
    write_station_info(client_identifier, output_filename)
    print("Done.")


if __name__ == "__main__":
    main()
