import sys
from enum import Enum
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
                               QSizePolicy, QMenuBar, QLabel)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QFont, QAction


class ButtonType(Enum):
    """按钮类型枚举"""
    NUMBER = "number"
    OPERATOR = "operator"
    SPECIAL = "special"
    EQUALS = "equals"


class StyleSheet:
    """样式表管理器 - 集中管理所有样式"""

    # 基础样式变量
    COLORS = {
        'primary_blue': '#0078d4',
        'primary_blue_hover': '#1a88e4',
        'primary_blue_pressed': '#005a9e',
        'orange': '#ff6b00',
        'orange_hover': '#ff7b20',
        'orange_pressed': '#e55100',
        'white': '#ffffff',
        'light_gray': '#f8f8f8',
        'medium_gray': '#e8e8e8',
        'dark_gray': '#d0d0d0',
        'text_dark': '#2c2c2c',
        'text_medium': '#404040',
        'text_light': '#666666',
    }

    # 通用渐变样式生成器
    @staticmethod
    def gradient_style(color1, color2, color3):
        return f"""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {color1}, stop:0.5 {color2}, stop:1 {color3});
        """

    # 使用属性或方法来定义样式，避免在类定义时调用静态方法
    @classmethod
    def get_window_style(cls):
        return f"""
            QMainWindow {{
                {cls.gradient_style(cls.COLORS['white'], cls.COLORS['light_gray'], cls.COLORS['medium_gray'])}
            }}
        """

    @classmethod
    def get_display_style(cls):
        return f"""
            QLineEdit {{
                font-size: 32px;
                font-weight: 600;
                {cls.gradient_style(cls.COLORS['white'], cls.COLORS['light_gray'], cls.COLORS['light_gray'])}
                border: 2px solid {cls.COLORS['dark_gray']};
                border-radius: 8px;
                padding: 15px;
                color: {cls.COLORS['text_dark']};
                selection-background-color: {cls.COLORS['primary_blue']};
            }}
        """

    @classmethod
    def get_operator_display_style(cls):
        return f"""
            QLabel {{
                font-size: 16px;
                color: {cls.COLORS['text_light']};
                background: transparent;
                padding: 5px 10px;
                min-height: 25px;
            }}
        """

    # 按钮基础样式模板
    @staticmethod
    def get_button_style(bg_colors, text_color="white", font_size=20, font_weight=600):
        normal_bg, hover_bg, pressed_bg = bg_colors
        return f"""
            QPushButton {{
                font-size: {font_size}px;
                font-weight: {font_weight};
                {StyleSheet.gradient_style(normal_bg[0], normal_bg[1], normal_bg[2])}
                color: {text_color};
                border: 1px solid {normal_bg[2]};
                border-radius: 12px;
                min-height: 60px;
                text-align: center;
            }}
            QPushButton:hover {{
                {StyleSheet.gradient_style(hover_bg[0], hover_bg[1], hover_bg[2])}
                border: 1px solid {hover_bg[2]};
                transform: translateY(-1px);
            }}
            QPushButton:pressed {{
                {StyleSheet.gradient_style(pressed_bg[0], pressed_bg[1], pressed_bg[2])}
                border: 1px solid {pressed_bg[2]};
                transform: translateY(1px);
            }}
        """


class CalculatorButton(QPushButton):
    """可复用的计算器按钮组件"""

    # 预定义按钮样式配置
    STYLE_CONFIG = {
        ButtonType.NUMBER: {
            'colors': (
                ('#ffffff', '#f8f8f8', '#e8e8e8'),
                ('#f0f8ff', '#e8f4ff', '#d8e8f8'),
                ('#d8e8f8', '#c8d8f0', '#b8c8e8')
            ),
            'text_color': '#2c2c2c',
            'font_size': 20
        },
        ButtonType.OPERATOR: {
            'colors': (
                ('#4a9eff', '#0078d4', '#005a9e'),
                ('#6bb6ff', '#1a88e4', '#0066b0'),
                ('#0066b0', '#005a9e', '#004080')
            ),
            'text_color': 'white',
            'font_size': 22,
            'font_weight': 700
        },
        ButtonType.SPECIAL: {
            'colors': (
                ('#f0f0f0', '#e0e0e0', '#d0d0d0'),
                ('#fff0f0', '#ffe0e0', '#ffd0d0'),
                ('#ffd0d0', '#ffc0c0', '#ffb0b0')
            ),
            'text_color': '#404040',
            'font_size': 18
        },
        ButtonType.EQUALS: {
            'colors': (
                ('#ff8c42', '#ff6b00', '#e55100'),
                ('#ffac72', '#ff7b20', '#f56100'),
                ('#f56100', '#e55100', '#d04100')
            ),
            'text_color': 'white',
            'font_size': 24,
            'font_weight': 700
        }
    }

    def __init__(self, text, button_type: ButtonType, callback=None):
        super().__init__(text)
        self.button_type = button_type
        self.setup_style()

        if callback:
            self.clicked.connect(callback)

    def setup_style(self):
        """设置按钮样式"""
        config = self.STYLE_CONFIG[self.button_type]
        style = StyleSheet.get_button_style(
            bg_colors=config['colors'],
            text_color=config['text_color'],
            font_size=config['font_size'],
            font_weight=config.get('font_weight', 600)
        )
        self.setStyleSheet(style)

class DisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()  # 添加这行来初始化界面

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 运算符显示
        self.operator_display = QLabel("")
        self.operator_display.setAlignment(Qt.AlignRight)
        self.operator_display.setStyleSheet(StyleSheet.get_operator_display_style())

        # 主显示屏
        self.main_display = QLineEdit()
        self.main_display.setText("0")
        self.main_display.setReadOnly(True)
        self.main_display.setAlignment(Qt.AlignRight)
        self.main_display.setStyleSheet(StyleSheet.get_display_style())
        self.main_display.setMinimumHeight(70)

        layout.addWidget(self.operator_display)
        layout.addWidget(self.main_display)

    def set_main_text(self, text):
        """设置主显示文本"""
        self.main_display.setText(text)

    def get_main_text(self):
        """获取主显示文本"""
        return self.main_display.text()

    def set_operator_text(self, text):
        """设置运算符显示文本"""
        self.operator_display.setText(text)

    def clear_operator_text(self):
        """清除运算符显示"""
        self.operator_display.setText("")


class ButtonGrid(QWidget):
    """可复用的按钮网格组件"""

    # 信号定义
    number_clicked = Signal(str)
    operator_clicked = Signal(str)
    equals_clicked = Signal()
    clear_clicked = Signal()
    clear_entry_clicked = Signal()
    backspace_clicked = Signal()
    decimal_clicked = Signal()
    plus_minus_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(8)

        # 按钮配置：(行, 列, 文本, 类型, 信号)
        button_configs = [
            # 第一行
            (0, 0, "CE", ButtonType.SPECIAL, self.clear_entry_clicked.emit),
            (0, 1, "C", ButtonType.SPECIAL, self.clear_clicked.emit),
            (0, 2, "⌫", ButtonType.SPECIAL, self.backspace_clicked.emit),
            (0, 3, "÷", ButtonType.OPERATOR, lambda: self.operator_clicked.emit("÷")),

            # 第二行
            (1, 0, "7", ButtonType.NUMBER, lambda: self.number_clicked.emit("7")),
            (1, 1, "8", ButtonType.NUMBER, lambda: self.number_clicked.emit("8")),
            (1, 2, "9", ButtonType.NUMBER, lambda: self.number_clicked.emit("9")),
            (1, 3, "×", ButtonType.OPERATOR, lambda: self.operator_clicked.emit("×")),

            # 第三行
            (2, 0, "4", ButtonType.NUMBER, lambda: self.number_clicked.emit("4")),
            (2, 1, "5", ButtonType.NUMBER, lambda: self.number_clicked.emit("5")),
            (2, 2, "6", ButtonType.NUMBER, lambda: self.number_clicked.emit("6")),
            (2, 3, "-", ButtonType.OPERATOR, lambda: self.operator_clicked.emit("-")),

            # 第四行
            (3, 0, "1", ButtonType.NUMBER, lambda: self.number_clicked.emit("1")),
            (3, 1, "2", ButtonType.NUMBER, lambda: self.number_clicked.emit("2")),
            (3, 2, "3", ButtonType.NUMBER, lambda: self.number_clicked.emit("3")),
            (3, 3, "+", ButtonType.OPERATOR, lambda: self.operator_clicked.emit("+")),

            # 第五行
            (4, 0, "±", ButtonType.SPECIAL, self.plus_minus_clicked.emit),
            (4, 1, "0", ButtonType.NUMBER, lambda: self.number_clicked.emit("0")),
            (4, 2, ".", ButtonType.NUMBER, self.decimal_clicked.emit),
            (4, 3, "=", ButtonType.EQUALS, self.equals_clicked.emit),
        ]

        # 创建按钮
        for row, col, text, btn_type, callback in button_configs:
            button = CalculatorButton(text, btn_type, callback)
            layout.addWidget(button, row, col)


class MenuManager:
    """菜单管理器 - 可复用的菜单组件"""

    def __init__(self, parent):
        self.parent = parent
        self.menubar = parent.menuBar()
        self.is_always_on_top = False
        self.setup_menus()

    def setup_menus(self):
        """设置菜单"""
        # 视图菜单
        view_menu = self.menubar.addMenu("视图(&V)")

        # 置顶功能
        self.always_on_top_action = QAction("置顶显示(&T)", self.parent)
        self.always_on_top_action.setCheckable(True)
        self.always_on_top_action.triggered.connect(self.toggle_always_on_top)
        view_menu.addAction(self.always_on_top_action)

        # 可以easily添加更多菜单项
        view_menu.addSeparator()

        # 主题菜单（示例扩展）
        theme_menu = view_menu.addMenu("主题(&H)")

        light_theme = QAction("浅色主题", self.parent)
        dark_theme = QAction("深色主题", self.parent)
        theme_menu.addAction(light_theme)
        theme_menu.addAction(dark_theme)

    def toggle_always_on_top(self):
        """切换置顶显示"""
        self.is_always_on_top = not self.is_always_on_top
        if self.is_always_on_top:
            self.parent.setWindowFlags(self.parent.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.parent.setWindowFlags(self.parent.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.parent.show()


class CalculatorLogic:
    """计算器逻辑 - 分离业务逻辑便于复用和测试"""

    def __init__(self):
        self.reset()

    def reset(self):
        """重置计算器状态"""
        self.current_input = ""
        self.previous_input = ""
        self.operator = ""
        self.result = 0
        self.should_reset_display = False

    def input_number(self, number, current_display):
        """处理数字输入"""
        if self.should_reset_display:
            return number

        if current_display == "0":
            return number
        else:
            return current_display + number

    def input_decimal(self, current_display):
        """处理小数点输入"""
        if self.should_reset_display:
            self.should_reset_display = False
            return "0."
        elif "." not in current_display:
            return current_display + "."
        return current_display

    def input_operator(self, op, current_display):
        """处理运算符输入"""
        if self.operator and not self.should_reset_display:
            # 连续运算
            result = self.calculate(current_display)
            if result is not None:
                self.previous_input = str(result)
            else:
                self.previous_input = current_display
        else:
            self.previous_input = current_display

        self.operator = op
        self.should_reset_display = True
        return self.previous_input, op

    def calculate(self, current_display):
        """执行计算"""
        if not self.operator or not self.previous_input:
            return None

        try:
            current = float(current_display)
            previous = float(self.previous_input)

            operations = {
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y,
                "×": lambda x, y: x * y,
                "÷": lambda x, y: x / y if y != 0 else None
            }

            if self.operator in operations:
                result = operations[self.operator](previous, current)
                if result is None:  # 除零错误
                    return "ERROR_DIVISION_BY_ZERO"

                self.operator = ""
                self.previous_input = ""
                self.should_reset_display = True

                # 格式化结果
                if isinstance(result, float) and result.is_integer():
                    return str(int(result))
                else:
                    return f"{result:.10g}"

        except (ValueError, ZeroDivisionError):
            return "ERROR"

        return None

    def toggle_sign(self, current_display):
        """切换正负号"""
        try:
            value = float(current_display)
            value = -value
            if value == int(value):
                return str(int(value))
            else:
                return str(value)
        except ValueError:
            return current_display

    def backspace(self, current_display):
        """退格操作"""
        if len(current_display) > 1:
            return current_display[:-1]
        else:
            return "0"


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("模块化精美计算器")
        self.setFixedSize(380, 550)
        self.setStyleSheet(StyleSheet.get_window_style())

        # 初始化组件
        self.logic = CalculatorLogic()
        self.menu_manager = MenuManager(self)

        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f8f8, stop:1 #eeeeee);
            }
        """)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 10, 15, 15)

        # 使用可复用组件
        self.display_widget = DisplayWidget()
        self.button_grid = ButtonGrid()

        layout.addWidget(self.display_widget)
        layout.addWidget(self.button_grid)

    def connect_signals(self):
        """连接信号和槽"""
        self.button_grid.number_clicked.connect(self.on_number_clicked)
        self.button_grid.operator_clicked.connect(self.on_operator_clicked)
        self.button_grid.equals_clicked.connect(self.on_equals_clicked)
        self.button_grid.clear_clicked.connect(self.on_clear_clicked)
        self.button_grid.clear_entry_clicked.connect(self.on_clear_entry_clicked)
        self.button_grid.backspace_clicked.connect(self.on_backspace_clicked)
        self.button_grid.decimal_clicked.connect(self.on_decimal_clicked)
        self.button_grid.plus_minus_clicked.connect(self.on_plus_minus_clicked)

    def on_number_clicked(self, number):
        """数字按钮处理"""
        new_display = self.logic.input_number(number, self.display_widget.get_main_text())
        self.display_widget.set_main_text(new_display)
        self.logic.should_reset_display = False

    def on_operator_clicked(self, operator):
        """运算符按钮处理"""
        result = self.logic.input_operator(operator, self.display_widget.get_main_text())
        if result:
            previous_num, op = result
            self.display_widget.set_operator_text(f"{previous_num} {op}")

    def on_equals_clicked(self):
        """等号按钮处理"""
        result = self.logic.calculate(self.display_widget.get_main_text())
        if result:
            if result == "ERROR_DIVISION_BY_ZERO":
                self.display_widget.set_main_text("错误：除零")
                self.logic.reset()
            elif result == "ERROR":
                self.display_widget.set_main_text("错误")
                self.logic.reset()
            else:
                self.display_widget.set_main_text(result)
            self.display_widget.clear_operator_text()

    def on_clear_clicked(self):
        """清除所有"""
        self.logic.reset()
        self.display_widget.set_main_text("0")
        self.display_widget.clear_operator_text()

    def on_clear_entry_clicked(self):
        """清除当前输入"""
        self.display_widget.set_main_text("0")

    def on_backspace_clicked(self):
        """退格处理"""
        new_display = self.logic.backspace(self.display_widget.get_main_text())
        self.display_widget.set_main_text(new_display)

    def on_decimal_clicked(self):
        """小数点处理"""
        new_display = self.logic.input_decimal(self.display_widget.get_main_text())
        self.display_widget.set_main_text(new_display)
        self.logic.should_reset_display = False

    def on_plus_minus_clicked(self):
        """正负号处理"""
        new_display = self.logic.toggle_sign(self.display_widget.get_main_text())
        self.display_widget.set_main_text(new_display)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("模块化精美计算器")
    app.setOrganizationName("Python学习")

    calculator = Calculator()
    calculator.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()