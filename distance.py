#requirments
import pandas as pd
import math
import maps

# Function to calculate distance between two points using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)*2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)*2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def getShortestDist(vLat,vLong):
    victim_lat = vLat
    victim_lon = vLong

    # Load police stations data from CSV
    police_stations = pd.read_csv("police_stations.csv")  # Update with your CSV filename
    police_locations = {}
    # Calculate distances between victim and police stations
    police_stations['distance'] = police_stations.apply(
        lambda row: haversine(victim_lat, victim_lon, row['latitude'], row['longitude']),
        axis=1
    )

    # Sort police stations by distance
    sorted_police_stations = police_stations.sort_values(by='distance')

    # Create list of dictionaries containing name, latitude, longitude, and distance
    nearest_police_stations_list = []
    for _, row in sorted_police_stations.iterrows():
        police_station = {
            'name': row['name'],
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'distance': row['distance']
        }
        nearest_police_stations_list.append(police_station)

    print("Nearest Police Stations:")
    for police_station in nearest_police_stations_list:
        print(f"{police_station['name']}: {police_station['distance']:.2f} km")

    return victim_lat, victim_lon, nearest_police_stations_list

if _name=="main_":
    vlan,vlon,npsl = getShortestDist(17.3,78.5)
    #dict = {ps1 : [lon, lat]}
    dic = {}
    for i in npsl:
        dic[i['name']]=[i['latitude'],i['longitude']]
    maps.show_map(17.3,78.5,dic)
