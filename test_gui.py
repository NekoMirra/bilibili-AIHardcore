#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyQt6 GUI测试脚本
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6测试窗口")
        self.setGeometry(100, 100, 400, 200)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加标签
        label = QLabel("这是一个测试窗口，如果你能看到这个窗口，说明PyQt6可以正常工作")
        layout.addWidget(label)
        
        # 添加按钮
        button = QPushButton("点击关闭")
        button.clicked.connect(self.close)
        layout.addWidget(button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec()) 