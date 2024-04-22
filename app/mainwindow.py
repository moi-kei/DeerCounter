from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from imageviewer import ImageViewer
from imagelistwidget import ImageListWidget
from webenginewidget import WebEngineWidget

class MainWindow(QMainWindow):
    """Main application window for DeerCounter."""

    def __init__(self):
        """Initialize the MainWindow."""
        super().__init__()

        self.setWindowTitle("DeerCounter")
        self.setGeometry(100, 100, 1400, 700)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Button to select a folder
        self.select_folder_btn = QPushButton("Select Folder", self)
        self.select_folder_btn.setFixedSize(100, 30)
        self.layout.addWidget(self.select_folder_btn)

        # Main layout for the image viewer, image list, and web map
        self.main_layout = QHBoxLayout()
        self.layout.addLayout(self.main_layout)

        # WebEngineWidget for displaying the folium map
        self.web_engine_widget = WebEngineWidget()
        self.main_layout.addWidget(self.web_engine_widget)

        # ImageViewer for displaying images
        self.image_viewer = ImageViewer(self)
        self.main_layout.addWidget(self.image_viewer)

        # ImageListWidget for displaying a list of images
        self.image_list_widget = ImageListWidget(self)
        self.main_layout.addWidget(self.image_list_widget)
        self.image_list_widget.setMaximumWidth(200)

        # Connect signals and slots
        self.select_folder_btn.clicked.connect(self.image_list_widget.select_folder)
        self.image_list_widget.image_paths_changed.connect(self.image_viewer.set_image_paths)
        self.image_viewer.image_changed.connect(self.web_engine_widget.update_map)
        self.image_list_widget.flight_path_changed.connect(self.web_engine_widget.set_flight_path)
        self.image_list_widget.image_clicked.connect(self.image_viewer.show_image)
        self.image_list_widget.image_clicked.connect(self.update_image_index)

    def update_image_index(self, image_path, index):
        """Update the current image index in the image viewer.

        Args:
            image_path (str): Path of the selected image.
            index (int): Index of the selected image.
        """
        self.image_viewer.current_index = index
