import sys
from PyQt6.QtWidgets import QApplication
from mainwindow import MainWindow

# Define the main function
def main():
    # Create a QApplication instance, passing command line arguments
    app = QApplication(sys.argv)
    
    # Create an instance of the MainWindow class
    window = MainWindow()
    
    # Make the main window visible
    window.show()
    
    # Start the application event loop and exit when it's done
    sys.exit(app.exec())

# Executes the main function if this script is run directly
if __name__ == "__main__":
    main()