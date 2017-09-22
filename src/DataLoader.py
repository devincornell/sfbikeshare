
import pandas as pd 
import numpy as np
import json

TRIP_DATA_FILE = 'data/trip.csv'
STATION_DATA_FILE = 'data/station.csv'
SCHOOL_DATA_FILE = 'data/Schools.csv'
BART_DATA_FILE = './data/BART Stations.csv'
TOUR_DATA_FILE = './data/Top 20 Attractions.csv'
ZONE_GEOJSON_FILE = './data/Zoning Districts.geojson'
INCOME_DATA = './data/income.csv'

def load_station_locations(filter_to_sf = True):
    df_station = pd.read_csv(STATION_DATA_FILE)
    if filter_to_sf:
        df_station = df_station[df_station.city == 'San Francisco']
    station_coords = list(zip(list(df_station.lat), list(df_station.long)))
    station_features = pd.DataFrame(station_coords, index = df_station.id)
    station_features.columns = ['lat', 'long']
    return station_features

def load_school_locations():
    df_school = pd.read_csv(SCHOOL_DATA_FILE)
    coord_strings = df_school['Location 1'].str.findall('CA\n\((.*),(.*)\)')
    school_coords = [(float(s[0][0]), float(s[0][1])) for s in coord_strings]
    return school_coords

def load_bart_locations():
    df_bart = pd.read_csv(BART_DATA_FILE)
    bart_coords = list(zip(list(df_bart.gtfs_latitude), list(df_bart.gtfs_longitude)))
    return bart_coords 

def load_tourist_locations():
    REGEX = '(.*). N, (.*). W'
    df_tour = pd.read_csv(TOUR_DATA_FILE)
    tour_strings = df_tour['Geographic Coordinates'].str.findall(REGEX)
    tour_coords = [(float(s[0][0]), -float(s[0][1])) for s in tour_strings]
    return tour_coords

def load_zones():
    with open(ZONE_GEOJSON_FILE, 'r') as fid:
        j = json.load(fid)
    return j['features']

def load_income_data():
    income_df_raw = pd.read_csv('./data/income.csv')
    idx = income_df_raw['Station ID']
    income_df = pd.DataFrame(index = idx)
    income_col = 'Per Capita Income (2013 Dollars)'
    income_df['income'] = pd.Series(income_df_raw[income_col].values, index = idx)
    return income_df

def load_ride_data():

    # Load rides data
    df_rides = pd.read_csv(TRIP_DATA_FILE)
    date_format = '%m/%d/%Y %H:%M'
    trip_starts = pd.to_datetime(df_rides.start_date, format = date_format)
    trip_ends = pd.to_datetime(df_rides.end_date, format = date_format)

    # Create feature data frame, indexed by trip ID
    features = pd.DataFrame(index = df_rides.index)

    # Feature 1: 1 for week day, 0 for weekend
    days_of_week = trip_starts.dt.dayofweek
    features['isweekday'] = days_of_week.isin(range(5))

    # Feature 2: Trip hour of day (0 to 23)
    features['hour'] = trip_starts.dt.hour

    # Feature 3: Trip duration (seconds)
    features['duration'] = df_rides.duration

    # Feature 4: Subscriber?
    features['subscriber'] = df_rides.subscription_type == 'Subscriber'

    # Source / dest station ids
    features['source'] = df_rides.start_station_id
    features['dest'] = df_rides.end_station_id

    return features