#requirements 
import folium
import webbrowser
import os

def pin_locations(lon, lan, locations_dict, map_title='Map'):
    # Create a map centered at the first location
    m = folium.Map(location=[lon, lan], zoom_start=15)

    # Add red marker for the given lon, lan
    folium.Marker(location=[lon, lan], popup='Pinned Location', icon=folium.Icon(color='red')).add_to(m)

    # Add blue markers for each location in the dictionary
    for key, value in locations_dict.items():
        folium.Marker(location=value, popup=f'{key}: {value}', icon=folium.Icon(color='blue')).add_to(m)

    # Save the map to an HTML file
    file_path = map_title + '.html'
    m.save(file_path)

    # Open the HTML file using the default web browser
    try:
        webbrowser.open('file://' + os.path.realpath(file_path))
    except Exception as e:
        print("Unable to open HTML file:", e)

def show_map(vlon, vlan, location_dict):
    pin_locations(vlon, vlan, location_dict,'Pinned_Locations')
