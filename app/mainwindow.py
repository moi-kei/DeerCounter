from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from imageviewer import ImageViewer
from imagelistwidget import ImageListWidget
from webenginewidget import WebEngineWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DeerCounter")
        self.setGeometry(100, 100, 1400, 700)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.select_folder_btn = QPushButton("Select Folder", self)
        self.select_folder_btn.setFixedSize(100, 30)
        self.layout.addWidget(self.select_folder_btn)

        # Main layout for the image viewer and image list
        self.main_layout = QHBoxLayout()
        self.layout.addLayout(self.main_layout)

        # Add WebEngineWidget for displaying folium map
        self.web_engine_widget = WebEngineWidget()
        self.main_layout.addWidget(self.web_engine_widget)

        # Add ImageViewer for displaying images
        self.image_viewer = ImageViewer(self)
        self.main_layout.addWidget(self.image_viewer)

        # Add ImageListWidget for displaying list of images
        self.image_list_widget = ImageListWidget(self)
        self.main_layout.addWidget(self.image_list_widget)
        self.image_list_widget.setMaximumWidth(200)

        self.select_folder_btn.clicked.connect(self.image_list_widget.select_folder)
        self.image_list_widget.image_paths_changed.connect(self.image_viewer.set_image_paths)
        self.image_viewer.image_changed.connect(self.web_engine_widget.update_map)
        self.image_list_widget.flight_path_changed.connect(self.web_engine_widget.set_flight_path)
        self.image_list_widget.image_clicked.connect(self.image_viewer.show_image)
        self.image_list_widget.image_clicked.connect(self.update_image_index)

    def update_image_index(self, image_path, index):
        self.image_viewer.current_index = index
