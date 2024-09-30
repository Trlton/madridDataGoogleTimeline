import xml.etree.ElementTree as ET
import pandas as pd
import datetime
import geopy.distance
import plotly.express as px


def parse_kml_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        placemarks = root.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
        data = []
        for placemark in placemarks:
            try:
                timestamp_element = placemark.find(
                    './/{http://www.opengis.net/kml/2.2}TimeStamp/{http://www.opengis.net/kml/2.2}when')
                timestamp = datetime.datetime.strptime(timestamp_element.text, '%Y-%m-%dT%H:%M:%SZ')
                coordinates_element = placemark.find(
                    './/{http://www.opengis.net/kml/2.2}Point/{http://www.opengis.net/kml/2.2}coordinates')
                coordinates = coordinates_element.text.split(',')[:2]
                data.append((timestamp, coordinates[0], coordinates[1]))
            except (AttributeError, ValueError) as e:
                print(f"Error parsing Placemark: {e}")

        return data
    except ET.ParseError as e:
        print(f"Error parsing KML file: {e}")
        return []


def process_data(data):
    # Clean data: remove invalid timestamps and coordinates
    cleaned_data = []
    for row in data:
        try:
            datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%SZ')
            float(row[1])
            float(row[2])
            cleaned_data.append(row)
        except (ValueError, TypeError):
            print("Invalid data:", row)

    # Calculate durations, distances, and total distance
    durations = []
    distances = []
    total_distance = 0
    for i in range(1, len(cleaned_data)):
        duration = cleaned_data[i][0] - cleaned_data[i - 1][0]
        durations.append(duration.total_seconds())
        coord1 = (cleaned_data[i - 1][1], cleaned_data[i - 1][2])
        coord2 = (cleaned_data[i][1], cleaned_data[i][2])
        distance = geopy.distance.distance(coord1, coord2).kilometers
        distances.append(distance)
        total_distance += distance

    # Calculate average speed
    total_time = sum(durations)
    if total_time > 0:
        average_speed = total_distance / (total_time / 3600)
    else:
        average_speed = 0  # Or raise an exception if appropriate

    # Identify frequent locations
    frequent_locations = pd.Series([tuple(point[1:]) for point in cleaned_data]).value_counts().head(5)

    # Print results
    print("Frequent locations:")
    print(frequent_locations)

    print("Total distance traveled:", total_distance, "km")
    print("Average speed:", average_speed, "km/h")

    # Visualize travel patterns (example using Plotly)
    df = pd.DataFrame(cleaned_data, columns=['timestamp', 'latitude', 'longitude'])
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='timestamp',
                            mapbox_style="open-street-map")
    fig.show()


file_paths = ['DataFiles/history-2024-09-15.kml', 'DataFiles/history-2024-09-16.kml', 'DataFiles/history-2024-09-17.kml', 'DataFiles/history-2024-09-18.kml', 'DataFiles/history-2024-09-19.kml']

for file_path in file_paths:
    data = parse_kml_file(file_path)
    process_data(data)