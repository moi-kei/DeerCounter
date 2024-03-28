import os
import exifread
from predict_image import predict_image

def get_flight_path(folder_path):
    flight_path = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            lat, lon = extract_gps(image_path)
            detected_objects = predict_image(image_path)
            midpoints = []
            for item in detected_objects:
                x_value = (item[0]+item[2])/2
                y_value = (item[1]+item[3])/2
                midpoints.append((x_value, y_value))
            if lat is not None and lon is not None:
                flight_path.append((filename, lat, lon, midpoints))
                print("filename: ", filename, " Latitude: ", lat, " Longitude: ", lon, "detected objects: ", midpoints)
    for item in flight_path:
        print("filename: ", item[0], " Latitude: ", item[1], " Longitude: ", item[2], "detected objects: ", item[3])
    return flight_path

def convert_invalid_coordinates(lat, lon):
    if lat > 90 or lon > 180:
        lat = lat / 10**7
        lon = lon / 10**7
    return lat, lon

def extract_gps(image_path):

    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
        latitude = tags.get('GPS GPSLatitude')
        longitude = tags.get('GPS GPSLongitude')

        if latitude and longitude:

            lat = float(latitude.values[0] + latitude.values[1] / 60 + latitude.values[2] / 3600)
            lon = float(longitude.values[0] + longitude.values[1] / 60 + longitude.values[2] / 3600)
            lat, lon = convert_invalid_coordinates(lat, lon)

            return lat, lon
        else:
            return None, None
