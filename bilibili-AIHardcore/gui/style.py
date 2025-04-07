"""
B站答题助手 GUI 样式定义
"""

# 应用全局样式
STYLE_SHEET = """
QMainWindow {
    background-color: #F5F5F5;
}

QTabWidget::pane {
    border: 1px solid #CCCCCC;
    background-color: white;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #E0E0E0;
    color: #333333;
    border: 1px solid #CCCCCC;
    border-bottom: none;
    padding: 8px 12px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom: 1px solid white;
}

QTabBar::tab:hover:!selected {
    background-color: #E8E8E8;
}

QFrame {
    border-radius: 4px;
    background-color: white;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1E88E5;
}

QPushButton:pressed {
    background-color: #1976D2;
}

QPushButton:disabled {
    background-color: #BDBDBD;
    color: #757575;
}

QLineEdit {
    padding: 6px;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    background-color: white;
}

QLineEdit:focus {
    border: 1px solid #2196F3;
}

QTextEdit {
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    background-color: white;
    padding: 4px;
}

QLabel {
    color: #424242;
}

QComboBox {
    padding: 6px;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    background-color: white;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    border: 1px solid #CCCCCC;
    selection-background-color: #2196F3;
    selection-color: white;
    border-radius: 0px;
}

/* 日志区域 */
QTextEdit#log_text {
    font-family: "Consolas", "Courier New", monospace;
    border: 1px solid #E0E0E0;
    background-color: #FAFAFA;
}
"""

# 深色主题样式（可选）
DARK_STYLE_SHEET = """
QMainWindow {
    background-color: #212121;
}

QTabWidget::pane {
    border: 1px solid #424242;
    background-color: #333333;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #424242;
    color: #E0E0E0;
    border: 1px solid #616161;
    border-bottom: none;
    padding: 8px 12px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #333333;
    border-bottom: 1px solid #333333;
}

QTabBar::tab:hover:!selected {
    background-color: #484848;
}

QFrame {
    border-radius: 4px;
    background-color: #333333;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1E88E5;
}

QPushButton:pressed {
    background-color: #1976D2;
}

QPushButton:disabled {
    background-color: #616161;
    color: #9E9E9E;
}

QLineEdit {
    padding: 6px;
    border: 1px solid #616161;
    border-radius: 4px;
    background-color: #424242;
    color: #E0E0E0;
}

QLineEdit:focus {
    border: 1px solid #2196F3;
}

QTextEdit {
    border: 1px solid #616161;
    border-radius: 4px;
    background-color: #424242;
    color: #E0E0E0;
    padding: 4px;
}

QLabel {
    color: #E0E0E0;
}

QComboBox {
    padding: 6px;
    border: 1px solid #616161;
    border-radius: 4px;
    background-color: #424242;
    color: #E0E0E0;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(down_arrow_dark.png);
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    border: 1px solid #616161;
    selection-background-color: #2196F3;
    selection-color: white;
    background-color: #424242;
    color: #E0E0E0;
    border-radius: 0px;
}

/* 日志区域 */
QTextEdit#log_text {
    font-family: "Consolas", "Courier New", monospace;
    border: 1px solid #424242;
    background-color: #212121;
    color: #E0E0E0;
}
""" 