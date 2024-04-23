import os
import exifread
import csv
from predict_image import predict_image

def get_flight_path(folder_path):
    """Extract flight path data from images in the specified folder.

    Args:
        folder_path (str): Path to the folder containing images.

    Returns:
        list: List of tuples representing the flight path data.
    """
    flight_path = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            lat, lon = extract_gps(image_path)
            detected_objects = predict_image(image_path)
            midpoints = []
            for item in detected_objects:
                x_value = (item[0] + item[2]) / 2
                y_value = (item[1] + item[3]) / 2
                midpoints.append((x_value, y_value))
            if lat is not None and lon is not None:
                flight_path.append((filename, lat, lon, len(midpoints)))
                print("filename: ", filename, " Latitude: ", lat, " Longitude: ", lon, "\ndetected objects: ", midpoints)
    
    # Create the CSV file with the name of the folder_path
    csv_file_name = os.path.join(folder_path, os.path.basename(folder_path) + '.csv')
    with open(csv_file_name, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)
        
        # Write the header row
        csv_writer.writerow(['Filename', 'Detected deer'])
        
        # Write each imaage name and neumber of deer in the flight path to the CSV file
        for item in flight_path:
            csv_writer.writerow([item[0], item[3]])
    return flight_path

def convert_invalid_coordinates(lat, lon):
    """Convert invalid GPS coordinates.

    This function was implemented after finding some of the GPS was recorded incorrectly in the images

    Args:
        lat (float): Latitude value.
        lon (float): Longitude value.

    Returns:
        tuple: Tuple containing converted latitude and longitude values.
    """
    if lat > 90 or lon > 180:
        lat = lat / 10**7
        lon = lon / 10**7
    return lat, lon

def extract_gps(image_path):
    """Extract GPS coordinates from the EXIF metadata of an image.

    Args:
        image_path (str): Path to the image file.

    Returns:
        tuple: Tuple containing latitude and longitude values.
    """
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

        '''
        This is code for the use of calculating the distance along the ground in an image
        This does not function correctly yet

        altitude = float(tags.get('GPS GPSAltitude').values[0])
        focal_length = tags.get('Image FocalLength').values[0]
        dpi_x = tags.get('Image XResolution').values[0]
        dpi_y = tags.get('Image YResolution').values[0]
        res_x = tags.get('EXIF ExifImageWidth').values[0]
        res_y = tags.get('EXIF ExifImageLength').values[0]
        centre_coords = (res_x/2, res_y/2)
        print(centre_coords)

        sensor_x = float(res_x / dpi_x)
        sensor_y = float(res_y / dpi_y)

        gsd_x = float((altitude * sensor_x) / ((focal_length/1000) * res_x))/100
        gsd_y = float((altitude * sensor_y) / ((focal_length/1000) * res_y))/100
        '''