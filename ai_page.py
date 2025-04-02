from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QScrollArea, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QPainter, QColor

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
        
        message = QLabel(text)
        message.setWordWrap(True)
        message.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        if is_user:
            self.layout.addStretch()
            self.layout.addWidget(message)
            self.layout.addLayout(self.icon_layout)
            style = """
                background-color: #444654;
                border-radius: 12px;
                padding: 12px;
                color: white;
            """
        else:
            self.layout.addLayout(self.icon_layout)
            self.layout.addWidget(message)
            self.layout.addStretch()
            style = """
                background-color: #343541;
                border-radius: 12px;
                padding: 12px;
                color: white;
            """
            
        self.setStyleSheet(f"QFrame {{ {style} }}")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    def update_icon(self, is_dark=True):
        pixmap = QIcon(self.icon_path).pixmap(QSize(24, 24))
        if not is_dark:
            # Aydınlık tema için ikonu #2198c1 rengine boyayalım
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
        
    def process_message(self, text):
        # Add user message
        self.chat_area.add_message(text, is_user=True)
        
        # Simulate AI response (replace with actual AI processing later)
        self.chat_area.add_message("Bu bir örnek AI yanıtıdır. Gerçek yanıt entegrasyonu yapılacak.", is_user=False)
    
    def apply_theme(self, is_dark):
        # Update background colors
        self.chat_area.update_style(is_dark)
        self.input_area.update_style(is_dark)
        
        # Update all icons
        self.input_area.update_icons(is_dark)
        
        # Update existing chat bubble icons
        for i in range(self.chat_area.chat_layout.count()):
            widget = self.chat_area.chat_layout.itemAt(i).widget()
            if isinstance(widget, ChatBubble):
                widget.update_icon(is_dark) 