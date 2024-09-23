import folium

# Load the KML file
kml_file = 'path/to/your/kml/file.kml'

# Create a new map
m = folium.Map(location=[40, -100], zoom_start=4)

# Add the KML file to the map
folium.Kml(kml_file, name='Google Timeline').add_to(m)

# Save the map as an HTML file
m.save('trip_overview.html')