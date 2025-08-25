from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("我的漂亮桌面软件")
        self.setFixedSize(400, 300)  # 固定窗口大小

        # 布局
        layout = QVBoxLayout()

        # 标签
        label = QLabel("欢迎使用 PySide6 桌面应用")
        label.setFont(QFont("微软雅黑", 14))
        label.setAlignment(Qt.AlignCenter)

        # 按钮
        btn = QPushButton("点击我")
        btn.setFont(QFont("微软雅黑", 12))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        btn.clicked.connect(self.on_button_click)

        # 添加控件到布局
        layout.addWidget(label)
        layout.addWidget(btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def on_button_click(self):
        print("按钮被点击了！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
