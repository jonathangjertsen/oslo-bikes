from typing import Any, Dict, List, Tuple

import geopandas
import pandas as pd
import numpy as np

StationInfo = Dict[str, Any]
Stations = Dict[int, StationInfo]
GeoLim = Tuple[float, float]
GeoRecord = Tuple[List[float], List[float]]

def read_availability_data(filename: str) -> pd.DataFrame:
    """Reads and cleans up the availability data stored in the file with the provided filename"""
    df = pd.read_csv(filename)
    df = df.drop_duplicates(subset=["timestamp", "station_id"])
    df = df.set_index(pd.to_datetime(df.timestamp.values, unit="s"))
    df["last_reported"] = pd.to_datetime(df.last_reported.values, unit="s")
    df = df.drop(columns=["timestamp"])
    return df


def read_station_data(filename: str) -> Stations:
    """Reads the station data in the file with the provided filename and returns a dict mapping station id to station info."""
    return {
        row.station_id: {
            key: value
            for key, value
            in row._asdict().items()
            if key != 'Index'
        }
        for row in pd.read_csv(filename).itertuples()
    }


def get_station_keys(stations: Stations) -> List[str]:
    """Returns the keys for a stations DataFrame."""
    for value in stations.values():
        return list(key for key in value.keys() if key != 'station_id')


def add_station_info(availability_df: pd.DataFrame, stations: Stations):
    """Adds station info to the provided availability DataFrame."""
    for key in get_station_keys(stations):
        availability_df["station_" + key] = availability_df.station_id.apply(lambda row: stations[row][key])


def read_augmented_availability_data(filename: str, station_filename: str) -> pd.DataFrame:
    """Reads and cleans up the availability data and station info and returns a DataFrame with the info."""
    availability_df = read_availability_data(filename)
    stations = read_station_data(station_filename)
    add_station_info(availability_df, stations)
    return availability_df


def timestamps(av_df: pd.DataFrame) -> list:
    """Returns every unique timestamp in the provided availability data."""
    return av_df.sort_index().index.unique()


def last_timestamp(av_df: pd.DataFrame):
    """Returns the last timestamp in the provided availability data."""
    return max(timestamps(av_df))


def last_snapshot(av_df: pd.DataFrame) -> pd.DataFrame:
    """Returns the last snapshot of the availability data."""
    return av_df[av_df.index == last_timestamp(av_df)]


def snapshots(av_df: pd.DataFrame):
    """Yields snapshots of the availability data in chronological order."""
    for timestamp in timestamps(av_df):
        yield av_df[av_df.index == timestamp]


def get_road_gdf(filename: str, xlim: GeoLim, ylim: GeoLim) -> geopandas.GeoDataFrame:
    """Reads the provided shapefile and sorts the data by arc length."""
    gdf = geopandas.read_file(filename)
    gdf = gdf[gdf.geometry.apply(lambda record: in_bounds(record, xlim, ylim))]
    gdf['arc_length'] = gdf.geometry.apply(lambda line: arc_length(line.xy))
    gdf = gdf.sort_values('arc_length', ascending=False)
    return gdf


def arc_length(record: GeoRecord) -> float:
    """Returns the arc length of a record."""
    x, y = record
    result: float = np.sum(
        [
            np.sqrt((x[i+1] - x[i]) ** 2 + (y[i+1] - y[i]) ** 2)
            for i in range(len(x) - 1)
        ]
    )
    return result


def in_bounds(geometry, xlim: GeoLim, ylim: GeoLim) -> bool:
    """Returns whether the provided geometry is entirely contained bounded by xlim and ylim."""
    x, y = geometry.xy
    return all(xlim[0] < xi < xlim[1] for xi in x) and all(ylim[0] < yi < ylim[1] for yi in y)

