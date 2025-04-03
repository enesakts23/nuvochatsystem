from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QScrollArea, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QPainter, QColor
import requests
import json

GEMINI_API_KEY = "AIzaSyDGGMxVE1OBp0A1ZI_hbIcjhJ12nLgM1-Y"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

class IconButton(QPushButton):
    def __init__(self, icon_path, size=24, tooltip=""):
        super().__init__()
        self.icon_path = f"resources/{icon_path}"
        self.size = size
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size + 12, size + 12)
        self.setToolTip(tooltip)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 16px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.update_icon()

    def update_icon(self, is_dark=True):
        pixmap = QIcon(self.icon_path).pixmap(QSize(self.size, self.size))
        if not is_dark:
            # Aydınlık tema için ikonu #2198c1 rengine boyayalım
            painter = QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), QColor("#2198c1"))
            painter.end()
        self.setIcon(QIcon(pixmap))

class ChatBubble(QFrame):
    def __init__(self, text, is_user=False):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.icon_layout = QVBoxLayout()
        self.icon_label = QLabel()
        self.icon_path = "resources/user.svg" if is_user else "resources/ai.svg"
        self.is_user = is_user
        self.update_icon()
        self.icon_layout.addWidget(self.icon_label)
        self.icon_layout.addStretch()
        
        message = QLabel()
        message.setWordWrap(True)
        message.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        message.setStyleSheet("QLabel { padding: 8px; }")
        message.setTextFormat(Qt.TextFormat.RichText)  # Enable HTML formatting
        message.setText(text)
        
        if is_user:
            self.layout.addStretch()
            self.layout.addWidget(message)
            self.layout.addLayout(self.icon_layout)
        else:
            self.layout.addLayout(self.icon_layout)
            self.layout.addWidget(message)
            self.layout.addStretch()
            
        self.update_style()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    def update_style(self, is_dark=True):
        if is_dark:
            user_bg = "#19C37D"  # Yeşil
            ai_bg = "#444654"    # Koyu gri
            text_color = "white"
            border = "none"
            shadow_color = "rgba(0, 0, 0, 0.3)"
        else:
            user_bg = "#19C37D"  # Yeşil
            ai_bg = "#F7F7F8"    # Açık gri
            text_color = "black" if not self.is_user else "white"
            border = "1px solid #E5E5E5"
            shadow_color = "rgba(0, 0, 0, 0.1)"
            
        style = f"""
            QFrame {{
                background-color: {user_bg if self.is_user else ai_bg};
                border-radius: 12px;
                padding: 12px;
                color: {text_color};
                border: {border};
                margin: 8px 0px;
            }}
            QFrame {{
                box-shadow: 0 2px 6px {shadow_color};
            }}
        """
        self.setStyleSheet(style)

    def update_icon(self, is_dark=True):
        pixmap = QIcon(self.icon_path).pixmap(QSize(24, 24))
        if not is_dark:
            if not self.is_user:  # Sadece AI ikonunu maviye boya
                painter = QPainter(pixmap)
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                painter.fillRect(pixmap.rect(), QColor("#2198c1"))
                painter.end()
        self.icon_label.setPixmap(pixmap)

class ChatArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.update_style()
        
        container = QWidget()
        self.chat_layout = QVBoxLayout(container)
        self.chat_layout.setContentsMargins(20, 20, 20, 20)  # Kenarlardan boşluk ekleyelim
        self.chat_layout.addStretch()
        self.setWidget(container)
        
    def update_style(self, is_dark=True):
        self.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {'#343541' if is_dark else 'white'};
            }}
            QWidget {{
                background-color: {'#343541' if is_dark else 'white'};
            }}
            QScrollBar:vertical {{
                border: none;
                background-color: {'#2A2B32' if is_dark else '#f0f0f0'};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {'#565869' if is_dark else '#c1c1c1'};
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """)
        
    def add_message(self, text, is_user=False):
        bubble = ChatBubble(text, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

class InputArea(QWidget):
    message_sent = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Mesajınızı yazın...")
        self.input_field.returnPressed.connect(self.send_message)
        self.update_style()
        
        self.attach_btn = IconButton("attach.svg", tooltip="Dosya ekle")
        self.mic_btn = IconButton("mic.svg", tooltip="Sesli mesaj")
        self.send_btn = IconButton("send.svg", tooltip="Gönder")
        self.send_btn.clicked.connect(self.send_message)
        
        layout.addWidget(self.attach_btn)
        layout.addWidget(self.input_field)
        layout.addWidget(self.mic_btn)
        layout.addWidget(self.send_btn)
    
    def update_style(self, is_dark=True):
        self.input_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {'#40414F' if is_dark else '#f0f0f0'};
                border: 1px solid {'#565869' if is_dark else '#e0e0e0'};
                border-radius: 12px;
                padding: 12px;
                color: {'white' if is_dark else 'black'};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 1px solid {'#565869' if is_dark else '#2198c1'};
            }}
        """)
        
        self.setStyleSheet(f"""
            InputArea {{
                background-color: {'#343541' if is_dark else 'white'};
                border-top: 1px solid {'#565869' if is_dark else '#e0e0e0'};
                padding: 10px;
            }}
        """)
    
    def update_icons(self, is_dark=True):
        self.attach_btn.update_icon(is_dark)
        self.mic_btn.update_icon(is_dark)
        self.send_btn.update_icon(is_dark)

    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            self.message_sent.emit(text)
            self.input_field.clear()

class AiPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Add chat area
        self.chat_area = ChatArea()
        layout.addWidget(self.chat_area)
        
        # Add input area
        self.input_area = InputArea()
        self.input_area.message_sent.connect(self.process_message)
        layout.addWidget(self.input_area)
        
        # Set initial light theme
        self.apply_theme(is_dark=False)
        
    def get_ai_response(self, user_message):
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            data = {
                "contents": [{
                    "parts": [{"text": user_message}]
                }]
            }
            
            response = requests.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if 'candidates' in response_data and len(response_data['candidates']) > 0:
                    return response_data['candidates'][0]['content']['parts'][0]['text']
            return "Üzgünüm, şu anda yanıt üretemiyorum. Lütfen tekrar deneyin."
        except Exception as e:
            print(f"Error: {str(e)}")
            return "Bir hata oluştu. Lütfen tekrar deneyin."
        
    def format_text(self, text):
        # Replace markdown with custom formatting
        formatted_text = text.replace('**', '')  # Remove bold markers
        
        # Add custom bullet points and indentation
        lines = formatted_text.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip().startswith('*'):
                # Convert markdown bullet points to custom style
                line = line.replace('*', '•', 1)
                line = '    ' + line  # Add indentation
            elif line.strip().endswith(':'):
                # Make headers more prominent
                line = f'<b>{line}</b>'
            formatted_lines.append(line)
        
        # Join lines with proper spacing
        formatted_text = '\n'.join(formatted_lines)
        
        # Add some basic HTML formatting
        formatted_text = formatted_text.replace('\n', '<br>')
        
        return formatted_text
        
    def process_message(self, text):
        # Add user message
        self.chat_area.add_message(text, is_user=True)
        
        # Get AI response using Gemini
        ai_response = self.get_ai_response(text)
        # Format the AI response
        formatted_response = self.format_text(ai_response)
        self.chat_area.add_message(formatted_response, is_user=False)
    
    def apply_theme(self, is_dark):
        # Update background colors
        self.chat_area.update_style(is_dark)
        self.input_area.update_style(is_dark)
        
        # Update all icons
        self.input_area.update_icons(is_dark)
        
        # Update existing chat bubble icons and styles
        for i in range(self.chat_area.chat_layout.count()):
            widget = self.chat_area.chat_layout.itemAt(i).widget()
            if isinstance(widget, ChatBubble):
                widget.update_icon(is_dark)
                widget.update_style(is_dark) 