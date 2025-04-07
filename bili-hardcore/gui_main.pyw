#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站答题助手图形界面版本 (.pyw格式，运行时不会显示终端窗口)
"""

import sys
import os

# 添加当前目录到模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 直接导入GUI模块
try:
    from gui.app import main
    
    if __name__ == "__main__":
        main()
except ImportError as e:
    # 如果发生导入错误，尝试显示错误对话框
    try:
        from PyQt6.QtWidgets import QApplication, QMessageBox
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "错误", f"无法启动程序: {str(e)}\n请确保已安装必要的依赖: pip install PyQt6")
    except:
        # 如果PyQt6也无法导入，只能将错误写入日志文件
        with open(os.path.join(current_dir, "gui_error.log"), "w") as f:
            f.write(f"启动错误: {str(e)}\n")
    sys.exit(1) 