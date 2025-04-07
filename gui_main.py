#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站答题助手图形界面版本
"""

import sys
import os
import subprocess
import platform

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 判断当前操作系统
is_windows = platform.system() == "Windows"

# 在Windows下，尝试使用无终端方式启动
if is_windows:
    # 构建.pyw文件路径
    pyw_path = os.path.join(current_dir, "bilibili-AIHardcore", "gui_main.pyw")
    if not os.path.exists(pyw_path):
        # 如果.pyw文件不存在，复制当前脚本内容为.pyw文件
        try:
            py_path = os.path.join(current_dir, "bilibili-AIHardcore", "gui_main.py")
            with open(py_path, 'r', encoding='utf-8') as src, open(pyw_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            print(f"已创建 {pyw_path}")
        except Exception as e:
            print(f"创建.pyw文件失败: {e}")
    
    # 使用pythonw.exe启动GUI应用，不显示终端
    try:
        # 使用pythonw.exe运行.pyw文件
        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(pythonw_path):
            # 尝试自动查找pythonw.exe
            python_dir = os.path.dirname(sys.executable)
            pythonw_path = os.path.join(python_dir, "pythonw.exe")
        
        if os.path.exists(pythonw_path):
            # 使用pythonw.exe启动应用
            subprocess.Popen([pythonw_path, pyw_path])
            sys.exit(0)
        else:
            print("未找到pythonw.exe，将使用普通方式启动")
    except Exception as e:
        print(f"启动无终端版本失败: {e}")

# 将bilibili-AIHardcore目录添加到Python模块搜索路径
bili_hardcore_dir = os.path.join(current_dir, "bilibili-AIHardcore")
sys.path.append(bili_hardcore_dir)

# 常规方式启动
try:
    # 尝试运行bilibili-AIHardcore/gui_main.py
    gui_main_path = os.path.join(bili_hardcore_dir, "gui_main.py")
    if os.path.exists(gui_main_path):
        print("正在启动B站答题助手图形界面...")
        # 使用utf-8编码读取文件
        try:
            with open(gui_main_path, 'r', encoding='utf-8') as f:
                code = compile(f.read(), gui_main_path, 'exec')
                exec(code)
        except Exception as e:
            print(f"执行gui_main.py失败: {e}")
    else:
        # 尝试直接导入模块
        print("正在尝试导入GUI模块...")
        try:
            from gui.app import main
            main()
        except ImportError as e:
            print(f"错误: 无法导入GUI模块: {e}")
            print("请确保已安装必要的依赖: pip install PyQt6")
            sys.exit(1)
except Exception as e:
    print(f"启动过程出现错误: {e}")
    sys.exit(1) 