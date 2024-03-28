import os
import exifread
from predict_image import predict_image

def get_flight_path(folder_path):
    coordinates = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            lat, lon = extract_gps(image_path)
            detected_objects = predict_image(image_path)
            if lat is not None and lon is not None:
                coordinates.append((filename, lat, lon, detected_objects))
                print("filename: ", filename, " Latitude: ", lat, " Longitude: ", lon, "detected objects: ", detected_objects)
    return coordinates

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
