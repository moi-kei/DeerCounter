from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QRadioButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from predict_image import predict_image
import os

class ImageViewer(QWidget):
    image_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_name_label = QLabel(self)  # Label to display the image name
        self.image_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prev_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)

        self.identify_deer_radio = QRadioButton("Identify deer (AI)", self)  # Radio button
        self.identify_deer_radio.setChecked(False)  # Initially unchecked

        self.prev_button.clicked.connect(self.prev_image)
        self.next_button.clicked.connect(self.next_image)
        self.identify_deer_radio.clicked.connect(lambda: self.show_image(self.image_paths[self.current_index]))

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.image_name_label)  # Add the image name label
        self.layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        self.layout.addLayout(button_layout)

        self.layout.addWidget(self.identify_deer_radio)  # Add the radio button

        self.image_paths = []
        self.current_index = 0
        self.current_image = ""  # Track the currently displayed image

    def show_image(self, image_path):
        if self.identify_deer_radio.isChecked():
            predicted_image = predict_image(image_path)  # Print the image path using the normal path
            pixmap = QPixmap(predicted_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()
            image_name = os.path.basename(predicted_image)
            self.current_image = image_name  # Update the currently displayed image
            self.image_name_label.setText(image_name)  # Update the image name label
            self.image_changed.emit(image_name)
            
        else:
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()
            image_name = os.path.basename(image_path)
            self.current_image = image_name  # Update the currently displayed image
            self.image_name_label.setText(image_name)  # Update the image name label
            self.image_changed.emit(image_name)

    def set_image_paths(self, image_paths):
        self.image_paths = image_paths
        if self.image_paths:
            self.show_image(self.image_paths[self.current_index])  # Show the first image

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image(self.image_paths[self.current_index])

    def next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_image(self.image_paths[self.current_index])
