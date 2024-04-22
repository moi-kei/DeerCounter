from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QRadioButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
import os

class ImageViewer(QWidget):
    """Widget for displaying images with navigation buttons and an option to identify deer."""

    # Signal emitted when the displayed image changes
    image_changed = pyqtSignal(str)  

    def __init__(self, parent=None):
        """Initialize the ImageViewer."""
        super().__init__(parent)
        
        # Label to display the image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label to display the image name
        self.image_name_label = QLabel(self)
        self.image_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Button to navigate to the previous image
        self.prev_button = QPushButton("Previous", self)
        # Button to navigate to the next image
        self.next_button = QPushButton("Next", self)

        # Radio button to enable AI identification
        self.identify_deer_radio = QRadioButton("Identify deer (AI)", self)
        # Initially checked
        self.identify_deer_radio.setChecked(True)

        # Connect signals and slots
        self.prev_button.clicked.connect(self.prev_image)
        self.next_button.clicked.connect(self.next_image)
        self.identify_deer_radio.clicked.connect(lambda: self.show_image(self.image_paths[self.current_index]))

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.image_name_label)
        self.layout.addWidget(self.image_label)

        # Layout for navigation buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        self.layout.addLayout(button_layout)

        # Add the radio button
        self.layout.addWidget(self.identify_deer_radio)

        # List to store image paths
        self.image_paths = []  
        # Index of the currently displayed image
        self.current_index = 0  
        # Name of the currently displayed image
        self.current_image = ""  

    def show_image(self, image_path):
        """Display the image specified by the given path.

        Args:
            image_path (str): Path of the image to display.
        """
        #if the identify deer radio is checked
        if self.identify_deer_radio.isChecked():
            #show the predicted image created by the model
            image_name = os.path.basename(image_path)
            predicted_image = 'predict/' + image_name
            pixmap = QPixmap(predicted_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()
            self.current_image = image_name
            self.image_name_label.setText(image_name)
            self.image_changed.emit(image_name)
        #if it is not
        else:
            #show the original image
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()
            image_name = os.path.basename(image_path)
            self.current_image = image_name
            self.image_name_label.setText(image_name)
            self.image_changed.emit(image_name)

    def set_image_paths(self, image_paths):
        """Set the list of image paths and display the first image."""
        self.image_paths = image_paths
        if self.image_paths:
            self.show_image(self.image_paths[self.current_index])

    def prev_image(self):
        """Display the previous image."""
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image(self.image_paths[self.current_index])

    def next_image(self):
        """Display the next image."""
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_image(self.image_paths[self.current_index])