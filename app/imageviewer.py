from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
import os

class ImageViewer(QWidget):
    image_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.prev_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)

        self.prev_button.clicked.connect(self.prev_image)
        self.next_button.clicked.connect(self.next_image)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        self.layout.addLayout(button_layout)

        self.image_paths = []
        self.current_index = 0
        self.current_image = ""  # Track the currently displayed image

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()
        image_name = os.path.basename(image_path)
        self.current_image = image_name  # Update the currently displayed image
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