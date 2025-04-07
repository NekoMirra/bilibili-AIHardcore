#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站答题助手图形界面版本
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
    print(f"错误: 无法导入GUI模块: {e}")
    print("请确保已安装必要的依赖: pip install PyQt6")
    sys.exit(1) 