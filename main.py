import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                           QVBoxLayout, QPushButton, QLabel, QStyle, QStackedWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

from ai_page import AiPage
from reports_page import ReportsPage
from settings_page import SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = False
        self.setWindowTitle("Şirket Yönetim Sistemi")
        self.showFullScreen()
        
        # Ana widget ve layout oluşturma
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header widget ve layout oluşturma
        self.header = QWidget()
        self.header.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: none;
            }
        """)
        header_height = 75
        self.header.setFixedHeight(header_height)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 0, 25, 0)
        header_layout.setSpacing(0)
        
        # Logo ekleme
        logo_label = QLabel()
        logo_label.setStyleSheet("border: none; background: transparent;")
        logo_pixmap = QPixmap("logo.png")
        logo_width = int(header_height * 2.5)
        scaled_logo = logo_pixmap.scaled(logo_width, header_height, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(scaled_logo)
        header_layout.addWidget(logo_label)
        
        # Boşluk ekleme
        header_layout.addStretch()
        
        # Kapatma butonu ekleme
        self.power_off_button = QPushButton()
        self.power_off_button.setIcon(QIcon("poweroff.png"))
        self.power_off_button.setIconSize(QSize(50, 50))
        self.power_off_button.setFixedSize(70, 70)
        self.power_off_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(224, 224, 224, 0.8);
                border-radius: 35px;
            }
        """)
        self.power_off_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.power_off_button.clicked.connect(self.close)
        header_layout.addWidget(self.power_off_button)
        
        # Header'ı ana layout'a ekleme
        main_layout.addWidget(self.header)
        
        # Content area with sidebar and main content
        content_area = QWidget()
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar oluşturma
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)  # Alt margin ekledik
        sidebar_layout.setSpacing(5)
        
        # Stacked widget for different pages
        self.stack = QStackedWidget()
        self.ai_page = AiPage()
        self.reports_page = ReportsPage()
        self.settings_page = SettingsPage()
        
        self.stack.addWidget(self.ai_page)
        self.stack.addWidget(self.reports_page)
        self.stack.addWidget(self.settings_page)
        
        # Sidebar menü öğeleri
        self.menu_buttons = []
        menu_items = [
            ("Yapay Zekaya Sor", "ai.png", 0),
            ("Raporlar", "report.png", 1),
            ("Ayarlar", "settings.png", 2)
        ]
        
        for text, icon, page_index in menu_items:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(20, 20))
            btn.clicked.connect(lambda checked, index=page_index: self.switch_page(index))
            btn.setProperty("Active", False)
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)
        
        # İlk butonu aktif yap
        self.menu_buttons[0].setProperty("Active", True)
        self.menu_buttons[0].setStyle(self.menu_buttons[0].style())
        
        sidebar_layout.addStretch()
        
        # Tema değiştirme butonu
        self.theme_button = QPushButton()
        self.theme_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        self.theme_button.setIconSize(QSize(20, 20))
        self.theme_button.setText("🌙 Koyu Tema" if not self.is_dark_theme else "☀️ Açık Tema")
        self.theme_button.clicked.connect(self.toggle_theme)
        sidebar_layout.addWidget(self.theme_button)
        
        # Layout'a ekleme
        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.stack)
        
        main_layout.addWidget(content_area)
        
        # Tema uygula
        self.apply_theme()
    
    def update_sidebar_style(self, sidebar):
        if self.is_dark_theme:
            sidebar.setStyleSheet("""
                QWidget {
                    background-color: #1a1a1a;
                    border-top-right-radius: 15px;
                }
                QPushButton {
                    color: white;
                    text-align: left;
                    padding: 12px 25px;
                    border: none;
                    font-size: 14px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
                QPushButton[Active=true] {
                    background-color: rgba(255, 255, 255, 0.2);
                }
            """)
        else:
            sidebar.setStyleSheet("""
                QWidget {
                    background-color: #2198c1;
                    border-top-right-radius: 15px;
                }
                QPushButton {
                    color: white;
                    text-align: left;
                    padding: 12px 25px;
                    border: none;
                    font-size: 14px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
                QPushButton[Active=true] {
                    background-color: rgba(255, 255, 255, 0.2);
                }
            """)
    
    def apply_theme(self):
        # Ana pencere arka plan rengi
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {'#121212' if self.is_dark_theme else 'white'};
            }}
        """)
        
        # Header stili
        self.header.setStyleSheet(f"""
            QWidget {{
                background-color: {'#1a1a1a' if self.is_dark_theme else 'white'};
                border-bottom: 2px solid {'#2c2c2c' if self.is_dark_theme else '#e0e0e0'};
            }}
        """)
        
        # Sidebar stili
        self.sidebar.setStyleSheet(f"""
            QWidget {{
                background-color: {'#1a1a1a' if self.is_dark_theme else '#2198c1'};
                border-right: 2px solid {'#2c2c2c' if self.is_dark_theme else '#e0e0e0'};
            }}
            QPushButton {{
                text-align: left;
                padding: 10px;
                border: none;
                border-radius: 5px;
                margin: 5px 10px;
                color: {'white' if self.is_dark_theme else 'white'};
                background-color: {'#1a1a1a' if self.is_dark_theme else '#2198c1'};
            }}
            QPushButton:hover {{
                background-color: {'#2c2c2c' if self.is_dark_theme else '#1a7a9f'};
            }}
            QPushButton[active="true"] {{
                background-color: {'#2c2c2c' if self.is_dark_theme else '#1a7a9f'};
                color: {'#4a9eff' if self.is_dark_theme else 'white'};
            }}
        """)
        
        # Theme button stili
        self.theme_button.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 10px;
                border: none;
                border-radius: 5px;
                margin: 5px 10px;
                color: {'white' if self.is_dark_theme else 'white'};
                background-color: {'#2c2c2c' if self.is_dark_theme else '#1a7a9f'};
            }}
            QPushButton:hover {{
                background-color: {'#363636' if self.is_dark_theme else '#156a8a'};
            }}
        """)
        
        # Power off button stili
        self.power_off_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                padding: 5px;
                border-radius: 5px;
                color: {'white' if self.is_dark_theme else 'black'};
                background-color: {'#1a1a1a' if self.is_dark_theme else 'white'};
            }}
            QPushButton:hover {{
                background-color: {'#2c2c2c' if self.is_dark_theme else '#f0f0f0'};
            }}
        """)
    
    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        
        # Update theme button text
        self.theme_button.setText("🌙 Koyu Tema" if not self.is_dark_theme else "☀️ Açık Tema")
        
        # Apply theme to all pages
        self.ai_page.apply_theme(self.is_dark_theme)
        self.reports_page.apply_theme(self.is_dark_theme)
        self.settings_page.apply_theme(self.is_dark_theme)
    
    def switch_page(self, index):
        # Önceki aktif butonu deaktif yap
        for btn in self.menu_buttons:
            btn.setProperty("Active", False)
            btn.setStyle(btn.style())
        
        # Yeni butonu aktif yap
        self.menu_buttons[index].setProperty("Active", True)
        self.menu_buttons[index].setStyle(self.menu_buttons[index].style())
        
        # Sayfayı değiştir
        self.stack.setCurrentIndex(index)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 