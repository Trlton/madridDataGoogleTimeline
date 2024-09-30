"""
Dette kode er i stor grad lavet ved hjælp af ChatGBT
Dette er basically en omskrevet mere clean version
Dette bruges for at se hvordan man kan bruge de forskellige funktioner i pykml og folium
Dette er ikke det færige produkt, men blot til at skabe forståelse
"""

import pykml as parser
import folium

dataFile = 'chosenFile'

with open(dataFile,'r') as f:
  root = parser.parse(f).getroot()

placemarks = root.Document.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
coordinates = []

# Place coordinates into coordinates list
for placemark in placemarks:
    coord_text = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates').text.strip()
    coords = [tuple(map(float, c.split(',')))[:2] for c in coord_text.split()] 
    coordinates.extend(coords)

# Position map and display route
centerMap = [coordinates[0][1], coordinates[0][0]]
m = folium.Map(location=centerMap, zoom_start=13)
folium.PolyLine(locations=[(lat, lon) for lon, lat in coordinates], color='blue').add_to(m)

# Saves and display map
m.save('route_map.html')
m.show_in_browser()
