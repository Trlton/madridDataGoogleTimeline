import folium
import os
from fastkml import kml

# Hostel coordinates (as midpoint)
hostel_coords = [40.41447396437289, -3.7036084441990917]

# Create a base map centered on the hostel with a reasonable zoom level
my_map = folium.Map(location=hostel_coords, zoom_start=14)

# Path to your KML file containing your walking routes
kml_file_path = 'DataFiles/history-2024-09-17.kml'

# Add the KML layer (walking routes)
if os.path.isfile(kml_file_path):
    with open(kml_file_path, 'rb') as file:  # Open the file as bytes ('rb')
        doc = file.read()
        # Parse the KML file as bytes
        k = kml.KML()
        k.from_string(doc.decode("utf-8"))  # Decode to string from bytes

        # Extract the placemarks and convert them to GeoJSON
        features = list(k.features())
        if features:
            for feature in features:
                for sub_feature in feature.features():
                    geo_json = sub_feature.geometry.geojson
                    folium.GeoJson(geo_json).add_to(my_map)
else:
    print(f"KML file not found at {kml_file_path}")

# Example locations with coordinates and image URLs (You can add more)
photo_locations = [
    {"coords": [40.4168, -3.7038], "image": "Fotos/ManMeat.jpg", "caption": "Location 1"},
    {"coords": [40.4122, -3.7070], "image": "Fotos/MAUNCH.jpg", "caption": "Location 2"},
]

# Add markers with images and hover popups
for loc in photo_locations:
    marker = folium.Marker(
        location=loc["coords"],
        popup=folium.Popup(f'<img src="{loc["image"]}" width="200"><br>{loc["caption"]}', max_width=250)
    )
    marker.add_to(my_map)

# Add a marker for your hostel
folium.Marker(
    location=hostel_coords,
    popup="My Hostel",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(my_map)

# Save the map to an HTML file
my_map.save('vacation_map_with_photos.html')

print("Map created and saved as 'vacation_map_with_photos.html'")
