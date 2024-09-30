from pykml import parser
import folium
import os
from geopy.distance import geodesic

# File paths for each day
kml_files = [
    'DataFiles/1Søndag.kml',
    'DataFiles/2Mandag.kml',
    'DataFiles/3Tirsdag.kml',
    'DataFiles/4Onsdag.kml',
    'DataFiles/5Torsdag.kml'
]

# Dictionary to hold coordinates and distances for each day
day_coordinates = {}
day_distances = {}

# Parse each KML file and extract coordinates
for i, kml_file in enumerate(kml_files):
    if os.path.isfile(kml_file):
        with open(kml_file, 'r') as f:
            root = parser.parse(f).getroot()

        placemarks = root.Document.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
        coordinates = []
        for placemark in placemarks:
            coord_text = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates').text.strip()
            coords = [tuple(map(float, c.split(',')))[:2] for c in coord_text.split()]  # Split longitude, latitude
            coordinates.extend(coords)

        # Store the coordinates for this day
        day_coordinates[f"Day {i + 1}"] = coordinates

        # Calculate the distance for the day
        total_distance = 0
        for j in range(1, len(coordinates)):
            total_distance += geodesic((coordinates[j - 1][1], coordinates[j - 1][0]),
                                       (coordinates[j][1], coordinates[j][0])).kilometers

        day_distances[f"Day {i + 1}"] = total_distance
    else:
        print(f"KML file not found: {kml_file}")

# Set the map center to the first day's first coordinate
if day_coordinates:
    first_day_coords = list(day_coordinates.values())[0]
    center_location = [first_day_coords[0][1], first_day_coords[0][0]]  # (latitude, longitude)
else:
    center_location = [0, 0]  # Default location if no coordinates found

# Create a folium map centered around the first point
m = folium.Map(location=center_location, zoom_start=13)

# Add routes for each day as separate FeatureGroups and display distance
for day, coords in day_coordinates.items():
    day_group = folium.FeatureGroup(name=day)

    # Create the polyline for the day's route
    folium.PolyLine(locations=[(lat, lon) for lon, lat in coords], color='blue').add_to(day_group)

    # Add a popup with the total distance for the day
    distance = day_distances[day]
    folium.Marker(
        location=[coords[0][1], coords[0][0]],  # Place the marker at the first point of the day
        popup=f"{day} - Total Distance: {distance:.2f} km"
    ).add_to(day_group)

    day_group.add_to(m)

# Add a LayerControl to toggle between days
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('multi_day_route_map_with_distance.html')
