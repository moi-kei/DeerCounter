from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
import folium

class WebEngineWidget(QWidget):
    def __init__(self, flight_path=None, parent=None):
        super().__init__(parent)
        
        self.flight_path = flight_path
        
        self.web_engine_view = QWebEngineView()
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.web_engine_view)

    def set_flight_path(self, flight_path):
        self.flight_path = flight_path  # Set the flight path list
        
    def update_map(self, image_name):
        m = folium.Map()

        max_lat, max_lon = -90, -180
        min_lat, min_lon = 90, 180

        # Initialize lists to hold coordinates for the polyline
        polyline_coords = []

        for item in self.flight_path:
            lat, lon = item[1], item[2]
            max_lat = max(max_lat, lat)
            max_lon = max(max_lon, lon)
            min_lat = min(min_lat, lat)
            min_lon = min(min_lon, lon)

            # Determine marker color
            marker_color = 'red' if item[0] == image_name else 'blue'

            popup = folium.Popup(item[0])
            folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color=marker_color)).add_to(m)

            # Add coordinates for the polyline
            polyline_coords.append([lat, lon])

        # Add polyline to the map
        folium.PolyLine(polyline_coords, color='blue').add_to(m)

        m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
        map_html = m.get_root().render()
        # Set HTML content with width and height of 100%
        html_content = f'<html><head><style>html, body, #map {{ width: 100%; height: 100%; margin: 0; padding: 0; }}</style></head><body><div id="map">{map_html}</div></body></html>'
        self.web_engine_view.setHtml(html_content)

            




    
