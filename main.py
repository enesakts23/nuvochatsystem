import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şirket Yönetim Sistemi")
        self.showFullScreen()
        self.setStyleSheet("background-color: white;")
        
        # Ana widget ve layout oluşturma
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header widget ve layout oluşturma
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border-bottom-left-radius: 15px;
                border-bottom-right-radius: 15px;
                border: none;
                border-bottom: 2px solid #2198c1;
            }
        """)
        header_height = 75
        header_widget.setFixedHeight(header_height)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 0, 25, 0)
        header_layout.setSpacing(0)
        
        # Logo ekleme
        logo_label = QLabel()
        logo_label.setStyleSheet("border: none; background: transparent;")  # Logo çerçevesini kaldır
        logo_pixmap = QPixmap("logo.png")
        logo_width = int(header_height * 2.5)
        scaled_logo = logo_pixmap.scaled(logo_width, header_height, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(scaled_logo)
        header_layout.addWidget(logo_label)
        
        # Boşluk ekleme
        header_layout.addStretch()
        
        # Kapatma butonu ekleme
        power_off_btn = QPushButton()
        power_off_btn.setIcon(QIcon("poweroff.png"))
        power_off_btn.setIconSize(QSize(50, 50))
        power_off_btn.setFixedSize(70, 70)
        power_off_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(224, 224, 224, 0.8);
                border-radius: 35px;
            }
        """)
        power_off_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        power_off_btn.clicked.connect(self.close)
        header_layout.addWidget(power_off_btn)
        
        # Header'ı ana layout'a ekleme
        main_layout.addWidget(header_widget)
        
        # İçerik alanı için boş widget
        content_widget = QWidget()
        content_widget.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(content_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 