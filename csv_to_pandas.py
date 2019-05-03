import pandas as pd


def read_availability_data(filename):
    df = pd.read_csv(filename)
    df = df.set_index(pd.to_datetime(df.timestamp.values, unit="s"))
    df["last_reported"] = pd.to_datetime(df.last_reported.values, unit="s")
    df = df.drop(columns=["timestamp"])
    return df


def read_station_data(filename):
    return {
        row.station_id: {
            key: value
            for key, value
            in row._asdict().items()
            if key != 'Index'
        }
        for row in pd.read_csv(filename).itertuples()
    }


def get_station_keys(stations):
    for value in stations.values():
        return list(key for key in value.keys() if key != 'station_id')


def add_station_info(availability_df, stations):
    for key in get_station_keys(stations):
        availability_df["station_" + key] = availability_df.station_id.apply(lambda row: stations[row][key])


def read_augmented_availability_data(filename, station_filename):
    availability_df = read_availability_data(filename)
    stations = read_station_data(station_filename)
    add_station_info(availability_df, stations)
    return availability_df
