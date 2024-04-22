from PyQt6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QFileDialog
from PyQt6.QtCore import pyqtSignal
import os
import shutil
from image_analyser import get_flight_path

class ImageListWidget(QWidget):
    """Widget for displaying a list of images and selecting a folder."""

    # Signals emitted by the widget
    # Signal emitted when a folder is selected
    folder_selected = pyqtSignal(str)  
    # Signal emitted when the list of image paths changes
    image_paths_changed = pyqtSignal(list)  
    # Signal emitted when an image is clicked (path and index)
    image_clicked = pyqtSignal(str, int) 
    # Signal emitted when the flight path changes
    flight_path_changed = pyqtSignal(list)  

    def __init__(self, parent=None):
        """Initialize the ImageListWidget."""
        super().__init__(parent)

        # List to store image paths
        self.image_paths = []  
        # Path of the selected folder
        self.folder_path = ""  

        #layout for the image list widget
        self.layout = QVBoxLayout(self)
        self.image_list_widget = QListWidget(self)
        self.layout.addWidget(self.image_list_widget)

        self.image_list_widget.itemClicked.connect(self.handle_item_click)

    def handle_item_click(self, item):
        """Handle the click event on an item in the image list."""
        # Get the index of the clicked item
        index = self.image_list_widget.row(item)
        # Get the image path from the clicked item
        image_path = os.path.normpath(os.path.join(self.folder_path, item.text()))
        # Emit the signal containing the image path and index
        self.image_clicked.emit(image_path, index)

    def select_folder(self):
        """Open a dialog to select a folder."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            # Emit signal for the selected folder
            self.folder_selected.emit(folder_path)  
            self.folder_path = folder_path
            try:
                # Remove the "predict" folder if it exists
                shutil.rmtree("predict")  
            except:
                None
            # Get flight path data for the selected folder
            flight_path = get_flight_path(folder_path)
            # Emit signal for the flight path
            self.flight_path_changed.emit(flight_path) 
            # Load images from the selected folder 
            self.load_images(folder_path)  

    def load_images(self, folder_path):
        """Load images from the specified folder."""
        # Clear the list of image paths
        self.image_paths.clear()  
         # Clear the list widget
        self.image_list_widget.clear() 

        image_extensions = [".png", ".jpg", ".jpeg"]

        # Iterate through files in the folder
        for file_name in os.listdir(folder_path):
            # Check if the file has an image extension
            if os.path.splitext(file_name)[1].lower() in image_extensions:
                # Add the file name to the list widget
                self.image_list_widget.addItem(file_name) 
                # Add the full path to the list 
                self.image_paths.append(os.path.join(folder_path, file_name))  

        # Emit signal with updated image paths
        self.image_paths_changed.emit(self.image_paths)  