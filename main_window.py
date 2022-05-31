import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog, QGraphicsScene
from PySide6.QtCore import Slot, Qt, QDir
from PySide6.QtGui import QPixmap, QIcon, QImageReader, QGuiApplication

class MainWindow():
    def __init__(self):
        # Load window from ui file
        loader = QUiLoader()
        self.w = loader.load("main_window.ui", None)

        # Setup window
        self.w.setWindowTitle("Pyside6 Template App")
        app_icon = QIcon()
        app_icon.addFile('icon.png')
        self.w.setWindowIcon(app_icon)

        # Setup window elements
        self.setup_window_elements()

        # Show window
        self.w.show()

    def setup_window_elements(self):
        # Setup 1st section

        # Connect push button actions to functions
        self.w.pushButton_addItem.clicked.connect(self.add_item_to_list)
        self.w.pushButton_deleteItem.clicked.connect(self.delete_item_from_list)

        # Setup 2nd section

        # Connect slider and spinbox actions to lambda functions
        self.w.horizontalSlider.valueChanged.connect(lambda l: self.w.doubleSpinBox.setValue( self.w.horizontalSlider.value() ))
        self.w.doubleSpinBox.valueChanged.connect(lambda l: self.w.horizontalSlider.setValue( self.w.doubleSpinBox.value() ))

        # Connect spinbox action to function by passing a parameter
        self.w.doubleSpinBox.valueChanged.connect(lambda l: self.update_lcd_display(self.w.doubleSpinBox.value()) )

        # Setup 3rd section

        # Set scene
        self.scene = QGraphicsScene()
        self.w.graphicsView.setScene(self.scene)

        self.w.pushButton_loadImage.clicked.connect(self.load_image)

    def load_image(self):
        # Select image with QFileDialog
        image_filename, image_extension = QFileDialog.getOpenFileName(self.w, "Open Image", ".", "Image Files (*.png *.jpg *.bmp)")
        print("Selected image filename:", image_filename)
        print("Selected image file extension:", image_extension)

        # Load image
        reader = QImageReader(image_filename)
        reader.setAutoTransform(True)
        new_image = reader.read()
        if (new_image.isNull()):
            print("Error: Image not found!")
            return
        
        # Clear the scene from all items
        self.scene.clear()

        # Convert image to QPixmap and add to the scene
        pixmap = QPixmap.fromImage(new_image)
        self.scene.addPixmap(pixmap)
        self.w.graphicsView.setSceneRect(0, 0, new_image.width(), new_image.height());
        
        # Fit QGraphicsView to the added pixmap
        first_item = self.w.graphicsView.items()[0]
        self.w.graphicsView.fitInView(first_item, Qt.KeepAspectRatio)

    @Slot()
    def add_item_to_list(self):
        input_text = self.w.lineEdit.text()
        if input_text != "":
            self.w.listWidget.addItem(input_text)
            self.w.lineEdit.setText("")
            print("Added item:", input_text)
        else:
            print("No items were added because input is empty!")

    @Slot()
    def delete_item_from_list(self):
        for item in self.w.listWidget.selectedItems():
            print("Removing item:", item.text())
            row_idx = self.w.listWidget.row(item)
            self.w.listWidget.takeItem(row_idx)

    @Slot()
    def update_lcd_display(self, new_value):
        self.w.lcdNumber.display(new_value)
