import sys
import qrcode
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLineEdit, QPushButton, QLabel)
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtCore import Qt, QByteArray
from io import BytesIO

class QRCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QuickyQR")
        self.setMinimumSize(400, 700)
        
        # Create a QLabel for the background
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("D:\programming\python\QRbackground.png"))
        self.background.setScaledContents(True)
        self.background.resize(self.size())


        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create input layout (horizontal)
        input_layout = QHBoxLayout()
        
        # Create text input
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text for QR code")
        input_layout.addWidget(self.text_input)
        
        # Create generate button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_qr_code)
        input_layout.addWidget(self.generate_button)
        
        # Add input layout to main layout
        main_layout.addLayout(input_layout)
        
        # Create QR code display label
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setMinimumSize(300, 300)
        main_layout.addWidget(self.qr_label)
        
        # Add a status label
        self.status_label = QLabel("Enter text and click Generate")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Connect enter key on text input to generate QR code
        self.text_input.returnPressed.connect(self.generate_qr_code)
        
    def generate_qr_code(self):
        """Generate QR code from text input and display it"""
        text = self.text_input.text().strip()
        
        if not text:
            self.status_label.setText("Please enter some text")
            self.qr_label.clear()
            return
        
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            # Create an image from the QR code
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert PIL image to QPixmap
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_data = buffer.getvalue()
            
            qimage = QImage.fromData(QByteArray(img_data))
            pixmap = QPixmap.fromImage(qimage)
            
            # Display QR code
            self.qr_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.status_label.setText(f"QR Code for: {text}")
            
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.qr_label.clear()

    def resizeEvent(self, event):
        # Resize background when window is resized
        self.background.resize(self.size())
        super().resizeEvent(event)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    icon = QIcon("D:\programming\python\QRicon.png")
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec())