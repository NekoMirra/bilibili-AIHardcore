#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建B站答题助手桌面快捷方式
"""

import os
import sys
import platform
import subprocess

def create_windows_shortcut():
    """在Windows上创建桌面快捷方式"""
    try:
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 构建.pyw文件路径
        pyw_path = os.path.join(current_dir, "gui_main.pyw")
        if not os.path.exists(pyw_path):
            # 如果.pyw文件不存在，复制当前脚本内容为.pyw文件
            try:
                py_path = os.path.join(current_dir, "gui_main.py")
                with open(py_path, 'r', encoding='utf-8') as src, open(pyw_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                print(f"已创建 {pyw_path}")
            except Exception as e:
                print(f"创建.pyw文件失败: {e}")
                return False
        
        # 查找pythonw.exe路径
        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(pythonw_path):
            # 尝试自动查找pythonw.exe
            python_dir = os.path.dirname(sys.executable)
            pythonw_path = os.path.join(python_dir, "pythonw.exe")
        
        if not os.path.exists(pythonw_path):
            print("未找到pythonw.exe，无法创建快捷方式")
            return False
        
        # 获取桌面路径
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop_path):
            # 可能是中文系统
            desktop_path = os.path.join(os.path.expanduser("~"), "桌面")
        
        if not os.path.exists(desktop_path):
            print("未找到桌面路径，无法创建快捷方式")
            return False
        
        # 快捷方式目标路径
        shortcut_path = os.path.join(desktop_path, "B站答题助手.lnk")
        
        # 使用PowerShell创建快捷方式
        ps_command = f'''
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "{pythonw_path}"
        $Shortcut.Arguments = "{pyw_path}"
        $Shortcut.WorkingDirectory = "{current_dir}"
        $Shortcut.Description = "B站答题助手"
        $Shortcut.Save()
        '''
        
        # 执行PowerShell命令
        subprocess.run(["powershell", "-Command", ps_command], check=True)
        
        print(f"桌面快捷方式已创建: {shortcut_path}")
        return True
    except Exception as e:
        print(f"创建快捷方式失败: {e}")
        return False

def create_linux_shortcut():
    """在Linux上创建桌面快捷方式"""
    try:
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 获取Python路径
        python_path = sys.executable
        
        # 桌面目录
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # .desktop文件路径
        desktop_file_path = os.path.join(desktop_path, "bili-hardcore.desktop")
        
        # .desktop文件内容
        desktop_content = f'''[Desktop Entry]
Type=Application
Name=B站答题助手
Comment=B站答题助手
Exec={python_path} {os.path.join(current_dir, "gui_main.py")}
Path={current_dir}
Terminal=false
Categories=Utility;
'''
        
        # 写入.desktop文件
        with open(desktop_file_path, 'w') as f:
            f.write(desktop_content)
        
        # 设置可执行权限
        os.chmod(desktop_file_path, 0o755)
        
        print(f"桌面快捷方式已创建: {desktop_file_path}")
        return True
    except Exception as e:
        print(f"创建快捷方式失败: {e}")
        return False

def create_macos_shortcut():
    """在macOS上创建应用程序快捷方式"""
    try:
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 获取Python路径
        python_path = sys.executable
        
        # 应用程序目录
        applications_path = "/Applications"
        
        # AppleScript内容
        script_content = f'''
        tell application "Finder"
            make new alias file at folder "{applications_path}" to file "{os.path.join(current_dir, "gui_main.py")}" with properties {{name:"B站答题助手"}}
        end tell
        '''
        
        # 临时脚本文件
        script_path = os.path.join(current_dir, "temp_script.scpt")
        
        # 写入脚本文件
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # 执行AppleScript
        subprocess.run(["osascript", script_path], check=True)
        
        # 删除临时脚本文件
        os.remove(script_path)
        
        print(f"应用程序快捷方式已创建: {os.path.join(applications_path, 'B站答题助手')}")
        return True
    except Exception as e:
        print(f"创建快捷方式失败: {e}")
        return False

if __name__ == "__main__":
    # 检测操作系统并创建相应的快捷方式
    system = platform.system()
    if system == "Windows":
        create_windows_shortcut()
    elif system == "Linux":
        create_linux_shortcut()
    elif system == "Darwin":  # macOS
        create_macos_shortcut()
    else:
        print(f"不支持的操作系统: {system}") 