import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
                               QSizePolicy, QMenuBar, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("精美计算器")
        self.setFixedSize(380, 520)

        # 初始化变量
        self.current_input = ""
        self.previous_input = ""
        self.operator = ""
        self.result = 0
        self.should_reset_display = False
        self.is_always_on_top = False

        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f5f5f5, stop:1 #e8e8e8);
            }
        """)

        self.init_ui()
        self.create_menu()

    def create_menu(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 视图菜单
        view_menu = menubar.addMenu("视图(&V)")

        # 置顶功能
        self.always_on_top_action = QAction("置顶显示(&T)", self)
        self.always_on_top_action.setCheckable(True)
        self.always_on_top_action.triggered.connect(self.toggle_always_on_top)
        view_menu.addAction(self.always_on_top_action)

    def toggle_always_on_top(self):
        """切换置顶显示"""
        self.is_always_on_top = not self.is_always_on_top
        if self.is_always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def init_ui(self):
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f8f8, stop:1 #eeeeee);
            }
        """)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 10, 15, 15)

        # 创建运算符显示区域
        self.operator_display = QLabel("")
        self.operator_display.setAlignment(Qt.AlignRight)
        self.operator_display.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666666;
                background: transparent;
                padding: 5px 10px;
                min-height: 25px;
            }
        """)
        main_layout.addWidget(self.operator_display)

        # 创建主显示屏
        self.display = QLineEdit()
        self.display.setText("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("""
            QLineEdit {
                font-size: 32px;
                font-weight: 600;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f8f8);
                border: 2px solid #d0d0d0;
                border-radius: 8px;
                padding: 15px;
                color: #2c2c2c;
                selection-background-color: #0078d4;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
            }
        """)
        self.display.setMinimumHeight(70)
        main_layout.addWidget(self.display)

        # 创建按钮布局
        button_layout = QGridLayout()
        button_layout.setSpacing(8)

        # 精美的按钮样式 - 扁平拟物风格
        number_button_style = """
            QPushButton {
                font-size: 20px;
                font-weight: 600;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:0.5 #f8f8f8, stop:1 #e8e8e8);
                border: 1px solid #d0d0d0;
                border-radius: 12px;
                min-height: 60px;
                color: #2c2c2c;
                text-align: center;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f8ff, stop:0.5 #e8f4ff, stop:1 #d8e8f8);
                border: 1px solid #4a9eff;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d8e8f8, stop:0.5 #c8d8f0, stop:1 #b8c8e8);
                border: 1px solid #2080ff;
                transform: translateY(1px);
            }
        """

        operator_button_style = """
            QPushButton {
                font-size: 22px;
                font-weight: 700;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a9eff, stop:0.5 #0078d4, stop:1 #005a9e);
                color: white;
                border: 1px solid #005a9e;
                border-radius: 12px;
                min-height: 60px;
                text-align: center;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6bb6ff, stop:0.5 #1a88e4, stop:1 #0066b0);
                border: 1px solid #0066b0;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0066b0, stop:0.5 #005a9e, stop:1 #004080);
                border: 1px solid #004080;
                transform: translateY(1px);
            }
        """

        special_button_style = """
            QPushButton {
                font-size: 18px;
                font-weight: 600;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f0f0, stop:0.5 #e0e0e0, stop:1 #d0d0d0);
                border: 1px solid #b0b0b0;
                border-radius: 12px;
                min-height: 60px;
                color: #404040;
                text-align: center;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fff0f0, stop:0.5 #ffe0e0, stop:1 #ffd0d0);
                border: 1px solid #ff6666;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffd0d0, stop:0.5 #ffc0c0, stop:1 #ffb0b0);
                border: 1px solid #ff4444;
                transform: translateY(1px);
            }
        """

        equals_button_style = """
            QPushButton {
                font-size: 24px;
                font-weight: 700;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff8c42, stop:0.5 #ff6b00, stop:1 #e55100);
                color: white;
                border: 1px solid #e55100;
                border-radius: 12px;
                min-height: 60px;
                text-align: center;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffac72, stop:0.5 #ff7b20, stop:1 #f56100);
                border: 1px solid #f56100;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f56100, stop:0.5 #e55100, stop:1 #d04100);
                border: 1px solid #d04100;
                transform: translateY(1px);
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
            (4, 3, "=", equals_button_style, self.equals_clicked),
        ]

        # 创建按钮
        for row, col, text, style, func in buttons:
            button = QPushButton(text)
            button.setStyleSheet(style)
            button.clicked.connect(func)
            button_layout.addWidget(button, row, col)

        main_layout.addLayout(button_layout)

    def update_operator_display(self, previous_num, operator):
        """更新运算符显示区域"""
        display_text = f"{previous_num} {operator}"
        self.operator_display.setText(display_text)

    def clear_operator_display(self):
        """清除运算符显示"""
        self.operator_display.setText("")

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

        # 更新运算符显示区域
        self.update_operator_display(self.previous_input, op)

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
                    self.clear_operator_display()
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
            self.clear_operator_display()

        except ValueError:
            self.display.setText("错误")
            self.clear_operator_display()
            self.clear_all()
        except Exception as e:
            self.display.setText("错误")
            self.clear_operator_display()
            self.clear_all()

    def clear_all(self):
        """清除所有内容"""
        self.display.setText("0")
        self.current_input = ""
        self.previous_input = ""
        self.operator = ""
        self.should_reset_display = False
        self.clear_operator_display()

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
    app.setApplicationName("精美计算器")
    app.setOrganizationName("Python学习")

    calculator = Calculator()
    calculator.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()