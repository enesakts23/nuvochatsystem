from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFormLayout, 
                             QLineEdit, QCheckBox, QPushButton, QComboBox)
from PyQt6.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Başlık
        self.title = QLabel("Ayarlar")
        self.update_title_style()
        layout.addWidget(self.title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Kullanıcı ayarları
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adınızı girin")
        form_layout.addRow("Kullanıcı Adı:", self.username_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email adresinizi girin")
        form_layout.addRow("Email:", self.email_input)
        
        # Tema seçimi
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Açık Tema", "Koyu Tema", "Sistem Teması"])
        form_layout.addRow("Tema:", self.theme_combo)
        
        # Bildirim ayarları
        self.notifications_checkbox = QCheckBox()
        self.notifications_checkbox.setChecked(True)
        form_layout.addRow("Bildirimleri Etkinleştir:", self.notifications_checkbox)
        
        # Form style
        self.update_input_styles()
        self.update_combo_style()
        self.update_checkbox_style()
        
        layout.addLayout(form_layout)
        
        # Kaydet butonu
        self.save_button = QPushButton("Kaydet")
        self.update_button_style()
        self.save_button.setFixedWidth(200)
        layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addStretch() 
    
    def update_title_style(self, is_dark=False):
        self.title.setStyleSheet(f"""
            QLabel {{
                color: {'white' if is_dark else '#2198c1'};
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
        """)
    
    def update_input_styles(self, is_dark=False):
        input_style = f"""
            QLineEdit {{
                padding: 8px;
                border: 2px solid {'#2c2c2c' if is_dark else '#e0e0e0'};
                border-radius: 5px;
                background-color: {'#1a1a1a' if is_dark else 'white'};
                color: {'white' if is_dark else 'black'};
                min-width: 250px;
            }}
            QLineEdit:focus {{
                border-color: {'#4a9eff' if is_dark else '#2198c1'};
            }}
        """
        self.username_input.setStyleSheet(input_style)
        self.email_input.setStyleSheet(input_style)
    
    def update_combo_style(self, is_dark=False):
        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px;
                border: 2px solid {'#2c2c2c' if is_dark else '#e0e0e0'};
                border-radius: 5px;
                background-color: {'#1a1a1a' if is_dark else 'white'};
                color: {'white' if is_dark else 'black'};
                min-width: 250px;
            }}
            QComboBox:focus {{
                border-color: {'#4a9eff' if is_dark else '#2198c1'};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
        """)
    
    def update_checkbox_style(self, is_dark=False):
        self.notifications_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {'white' if is_dark else 'black'};
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {'#2c2c2c' if is_dark else '#e0e0e0'};
                border-radius: 5px;
                background-color: {'#1a1a1a' if is_dark else 'white'};
            }}
            QCheckBox::indicator:checked {{
                background-color: {'#4a9eff' if is_dark else '#2198c1'};
                border-color: {'#4a9eff' if is_dark else '#2198c1'};
            }}
        """)
    
    def update_button_style(self, is_dark=False):
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                padding: 10px 20px;
                background-color: {'#4a9eff' if is_dark else '#2198c1'};
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {'#3a7fcf' if is_dark else '#1a7a9f'};
            }}
        """)
    
    def apply_theme(self, is_dark):
        self.update_title_style(is_dark)
        self.update_input_styles(is_dark)
        self.update_combo_style(is_dark)
        self.update_checkbox_style(is_dark)
        self.update_button_style(is_dark) 