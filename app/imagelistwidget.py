from PyQt6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QFileDialog
from PyQt6.QtCore import pyqtSignal
import os
import shutil
from gps_extractor import get_flight_path

class ImageListWidget(QWidget):
    folder_selected = pyqtSignal(str)
    image_paths_changed = pyqtSignal(list)
    image_clicked = pyqtSignal(str, int) 
    flight_path_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.image_paths = []
        self.folder_path = ""

        self.layout = QVBoxLayout(self)
        self.image_list_widget = QListWidget(self)
        self.layout.addWidget(self.image_list_widget)

        self.image_list_widget.itemClicked.connect(self.handle_item_click)


    def handle_item_click(self, item):
        # Get the index of the clicked item
        index = self.image_list_widget.row(item)
        # Get the image path from the clicked item
        image_path = os.path.normpath(os.path.join(self.folder_path, item.text()))
        # Emit the signal containing the image path and index
        self.image_clicked.emit(image_path, index)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_selected.emit(folder_path)
            self.folder_path = folder_path
            try:
                shutil.rmtree("predict")
            except:
                None
            flight_path = get_flight_path(folder_path)
            self.flight_path_changed.emit(flight_path)
            self.load_images(folder_path)

    def load_images(self, folder_path):
        self.image_paths.clear()
        self.image_list_widget.clear()

        image_extensions = [".png", ".jpg", ".jpeg"]

        for file_name in os.listdir(folder_path):
            if os.path.splitext(file_name)[1].lower() in image_extensions:
                self.image_list_widget.addItem(file_name)
                self.image_paths.append(os.path.join(folder_path, file_name))

        self.image_paths_changed.emit(self.image_paths)