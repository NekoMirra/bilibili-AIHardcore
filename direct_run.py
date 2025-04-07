#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
直接运行B站答题助手GUI
"""

import sys
import os
import traceback

# 获取当前目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 添加bili-hardcore目录到模块搜索路径
bili_hardcore_dir = os.path.join(current_dir, "bili-hardcore")
sys.path.append(bili_hardcore_dir)

# 直接导入GUI模块
try:
    print("成功导入GUI模块，正在启动应用程序...")
    
    # 导入应用程序主模块
    from gui.app import main
    
    # 运行应用程序
    main()
except ImportError as e:
    print(f"导入错误: {e}")
    print("详细错误信息:")
    traceback.print_exc()
    print("\n尝试解决方案:")
    print("1. 确保已安装PyQt6: pip install PyQt6")
    print("2. 确保目录结构正确:")
    print(f"   - 检查 {os.path.join(bili_hardcore_dir, 'gui', 'app.py')} 是否存在")
except Exception as e:
    print(f"运行错误: {e}")
    print("详细错误信息:")
    traceback.print_exc() 