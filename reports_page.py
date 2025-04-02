from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Başlık
        self.title = QLabel("Raporlar")
        self.update_title_style()
        layout.addWidget(self.title)
        
        # Tablo oluşturma
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Rapor Adı", "Oluşturma Tarihi", "Boyut", "Durum"])
        
        # Örnek veriler
        sample_data = [
            ["Aylık Analiz", "2024-04-02", "2.5 MB", "Tamamlandı"],
            ["Haftalık Özet", "2024-04-01", "1.2 MB", "Tamamlandı"],
            ["Günlük Rapor", "2024-04-02", "0.8 MB", "İşleniyor"]
        ]
        
        self.table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
        
        self.update_table_style()
        
        # Sütun genişliklerini ayarla
        self.table.horizontalHeader().setStretchLastSection(True)
        for i in range(self.table.columnCount() - 1):
            self.table.setColumnWidth(i, 200)
            
        layout.addWidget(self.table)
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
    
    def update_table_style(self, is_dark=False):
        self.table.setStyleSheet(f"""
            QTableWidget {{
                border: 2px solid {'#2c2c2c' if is_dark else '#e0e0e0'};
                border-radius: 10px;
                padding: 10px;
                background-color: {'#1a1a1a' if is_dark else 'white'};
                color: {'white' if is_dark else 'black'};
                gridline-color: {'#2c2c2c' if is_dark else '#e0e0e0'};
            }}
            QTableWidget::item {{
                padding: 10px;
                color: {'white' if is_dark else 'black'};
            }}
            QHeaderView::section {{
                background-color: {'#2c2c2c' if is_dark else '#2198c1'};
                color: white;
                padding: 10px;
                border: none;
            }}
        """)
    
    def apply_theme(self, is_dark):
        self.update_title_style(is_dark)
        self.update_table_style(is_dark) 