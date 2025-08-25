import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
                               QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算器")
        self.setFixedSize(350, 450)

        # 初始化变量
        self.current_input = ""
        self.previous_input = ""
        self.operator = ""
        self.result = 0
        self.should_reset_display = False

        self.init_ui()

    def init_ui(self):
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建显示屏
        self.display = QLineEdit()
        self.display.setText("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                font-weight: bold;
                background-color: white;
                border: 2px solid #ccc;
                padding: 10px;
                color: black;
            }
        """)
        self.display.setMinimumHeight(60)
        main_layout.addWidget(self.display)

        # 创建按钮布局
        button_layout = QGridLayout()
        button_layout.setSpacing(3)

        # 按钮样式
        number_button_style = """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """

        operator_button_style = """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                background-color: #0078d4;
                color: white;
                border: 1px solid #0078d4;
                border-radius: 5px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """

        special_button_style = """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #e1e1e1;
                border: 1px solid #ccc;
                border-radius: 5px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #d1d1d1;
            }
            QPushButton:pressed {
                background-color: #c1c1c1;
            }
        """

        # 定义按钮布局 (行, 列, 文本, 样式, 连接函数)
        buttons = [
            # 第一行
            (0, 0, "CE", special_button_style, self.clear_entry),
            (0, 1, "C", special_button_style, self.clear_all),
            (0, 2, "⌫", special_button_style, self.backspace),
            (0, 3, "÷", operator_button_style, lambda: self.operator_clicked("÷")),

            # 第二行
            (1, 0, "7", number_button_style, lambda: self.number_clicked("7")),
            (1, 1, "8", number_button_style, lambda: self.number_clicked("8")),
            (1, 2, "9", number_button_style, lambda: self.number_clicked("9")),
            (1, 3, "×", operator_button_style, lambda: self.operator_clicked("×")),

            # 第三行
            (2, 0, "4", number_button_style, lambda: self.number_clicked("4")),
            (2, 1, "5", number_button_style, lambda: self.number_clicked("5")),
            (2, 2, "6", number_button_style, lambda: self.number_clicked("6")),
            (2, 3, "-", operator_button_style, lambda: self.operator_clicked("-")),

            # 第四行
            (3, 0, "1", number_button_style, lambda: self.number_clicked("1")),
            (3, 1, "2", number_button_style, lambda: self.number_clicked("2")),
            (3, 2, "3", number_button_style, lambda: self.number_clicked("3")),
            (3, 3, "+", operator_button_style, lambda: self.operator_clicked("+")),

            # 第五行
            (4, 0, "±", special_button_style, self.plus_minus),
            (4, 1, "0", number_button_style, lambda: self.number_clicked("0")),
            (4, 2, ".", number_button_style, self.decimal_clicked),
            (4, 3, "=", operator_button_style, self.equals_clicked),
        ]

        # 创建按钮
        for row, col, text, style, func in buttons:
            button = QPushButton(text)
            button.setStyleSheet(style)
            button.clicked.connect(func)
            button_layout.addWidget(button, row, col)

        main_layout.addLayout(button_layout)

    def number_clicked(self, number):
        """处理数字按钮点击"""
        if self.should_reset_display:
            self.display.setText("")
            self.should_reset_display = False

        current_text = self.display.text()
        if current_text == "0":
            self.display.setText(number)
        else:
            self.display.setText(current_text + number)

    def decimal_clicked(self):
        """处理小数点按钮点击"""
        current_text = self.display.text()
        if self.should_reset_display:
            self.display.setText("0.")
            self.should_reset_display = False
        elif "." not in current_text:
            self.display.setText(current_text + ".")

    def operator_clicked(self, op):
        """处理运算符按钮点击"""
        if self.operator and not self.should_reset_display:
            self.equals_clicked()

        self.previous_input = self.display.text()
        self.operator = op
        self.should_reset_display = True

    def equals_clicked(self):
        """处理等号按钮点击"""
        if not self.operator or not self.previous_input:
            return

        try:
            current = float(self.display.text())
            previous = float(self.previous_input)

            if self.operator == "+":
                result = previous + current
            elif self.operator == "-":
                result = previous - current
            elif self.operator == "×":
                result = previous * current
            elif self.operator == "÷":
                if current == 0:
                    self.display.setText("错误：除零")
                    self.clear_all()
                    return
                result = previous / current
            else:
                return

            # 格式化结果显示
            if result.is_integer():
                self.display.setText(str(int(result)))
            else:
                self.display.setText(f"{result:.10g}")

            self.operator = ""
            self.previous_input = ""
            self.should_reset_display = True

        except ValueError:
            self.display.setText("错误")
            self.clear_all()
        except Exception as e:
            self.display.setText("错误")
            self.clear_all()

    def clear_all(self):
        """清除所有内容"""
        self.display.setText("0")
        self.current_input = ""
        self.previous_input = ""
        self.operator = ""
        self.should_reset_display = False

    def clear_entry(self):
        """清除当前输入"""
        self.display.setText("0")

    def backspace(self):
        """退格操作"""
        current_text = self.display.text()
        if len(current_text) > 1:
            self.display.setText(current_text[:-1])
        else:
            self.display.setText("0")

    def plus_minus(self):
        """正负号切换"""
        current_text = self.display.text()
        try:
            value = float(current_text)
            value = -value
            if value.is_integer():
                self.display.setText(str(int(value)))
            else:
                self.display.setText(str(value))
        except ValueError:
            pass


def main():
    app = QApplication(sys.argv)

    # 设置应用程序图标和名称
    app.setApplicationName("计算器")
    app.setOrganizationName("Python学习")

    calculator = Calculator()
    calculator.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()