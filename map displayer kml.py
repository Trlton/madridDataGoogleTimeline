from pykml import parser

# Load and parse the KML file
with open('data.kml', 'r') as f:
    root = parser.parse(f).getroot()

# Example: Accessing the Placemark elements and extracting coordinates
placemarks = root.Document.findall('.//{http://www.opengis.net/kml/2.2}Placemark')

coordinates = []
for placemark in placemarks:
    coord_text = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates').text.strip()
    coords = [tuple(map(float, c.split(',')))[:2] for c in coord_text.split()]  # Split longitude, latitude
    coordinates.extend(coords)

# Now 'coordinates' holds a list of (longitude, latitude) tuples
print(coordinates)


import folium

# Center the map on the first coordinate
center_location = [coordinates[0][1], coordinates[0][0]]  # (latitude, longitude)

# Create a folium map centered around the first point in the route
m = folium.Map(location=center_location, zoom_start=13)

# Add the route as a PolyLine
folium.PolyLine(locations=[(lat, lon) for lon, lat in coordinates], color='blue').add_to(m)

# Save or display the map
m.save('route_map.html')
m.show_in_browser()
# If you're running this in a Jupyter Notebook or IPython environment
