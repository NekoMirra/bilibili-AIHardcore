import sys
import os
import threading
import qrcode
from io import BytesIO
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QComboBox, 
                             QLineEdit, QTextEdit, QTabWidget, QFrame, 
                             QScrollArea, QMessageBox, QStackedWidget,
                             QDialog, QFormLayout, QDialogButtonBox)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QSize, QThread
from PyQt6.QtGui import QIcon, QPixmap, QFont, QTextCursor

# 导入样式
from .style import STYLE_SHEET

# 导入bili-hardcore的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.login import auth, is_login, logout
from scripts.start_senior import QuizSession
from tools.logger import logger
from config.config import (load_api_key, save_api_key, load_model_config, 
                          save_model_config, MODEL_CONFIGS, model_choice, API_KEY_GEMINI, API_KEY_DEEPSEEK, API_KEY_CUSTOM, CUSTOM_MODEL_CONFIG)

# 自定义日志捕获类，用于将日志重定向到GUI
class LogHandler(QObject):
    log_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.buffer = []
    
    def write(self, text):
        if text.strip():
            self.log_signal.emit(text)
            self.buffer.append(text)
    
    def flush(self):
        pass

# 二维码登录对话框
class QRCodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.url = None
        self.login_result = False
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("B站扫码登录")
        self.setMinimumSize(280, 350)
        
        layout = QVBoxLayout(self)
        
        # 提示文本
        hint_label = QLabel("请使用哔哩哔哩APP扫描二维码登录")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint_label)
        
        # 二维码图像容器
        qr_container = QFrame()
        qr_container.setFrameShape(QFrame.Shape.StyledPanel)
        qr_container.setStyleSheet("background-color: white;")
        qr_layout = QVBoxLayout(qr_container)
        
        self.qrcode_label = QLabel()
        self.qrcode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qrcode_label.setFixedSize(200, 200)
        qr_layout.addWidget(self.qrcode_label)
        
        layout.addWidget(qr_container)
        
        # 状态提示
        self.status_label = QLabel("等待扫码...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)  # 允许文本换行
        layout.addWidget(self.status_label)
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)
    
    def set_qr_code(self, url):
        """设置二维码图像"""
        self.url = url
        
        # 生成二维码图像
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,  # 减小盒子大小
            border=2,    # 减小边框宽度
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # 创建图像
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 将PIL图像转换为QPixmap
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        
        # 限制二维码尺寸，确保适合窗口
        scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        
        # 显示二维码
        self.qrcode_label.setPixmap(scaled_pixmap)
        
        # 以文本方式也显示链接
        self.status_label.setText(f"<a href='{url}'>点击这里直接打开链接进行登录</a>")
        self.status_label.setOpenExternalLinks(True)
    
    def set_status(self, status):
        """设置状态提示文本"""
        self.status_label.setText(status)
    
    def set_login_result(self, success):
        """设置登录结果"""
        self.login_result = success
        if success:
            self.set_status("登录成功！")
            self.accept()
        else:
            self.set_status("登录失败，请重试")

# 验证码输入对话框
class CaptchaDialog(QDialog):
    def __init__(self, url=None, categories=None, parent=None):
        super().__init__(parent)
        self.url = url
        self.categories = categories
        self.captcha_text = ""
        self.category_ids = ""
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("验证码")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 显示分类信息
        if self.categories:
            cats_label = QLabel("请选择以下分类ID:")
            layout.addWidget(cats_label)
            
            cats_text = QTextEdit()
            cats_text.setReadOnly(True)
            cats_text.setMaximumHeight(120)
            
            cats_info = ""
            for cat in self.categories:
                cats_info += f"ID: {cat.get('id')} - {cat.get('name')}\n"
            cats_text.setText(cats_info)
            layout.addWidget(cats_text)
            
            id_label = QLabel("输入分类ID (多个ID用英文逗号隔开):")
            layout.addWidget(id_label)
            
            self.id_input = QLineEdit()
            layout.addWidget(self.id_input)
        
        # 显示验证码链接
        if self.url:
            url_label = QLabel(f"验证码链接: <a href='{self.url}'>{self.url}</a>")
            url_label.setOpenExternalLinks(True)
            layout.addWidget(url_label)
        
        # 验证码输入
        captcha_label = QLabel("输入验证码:")
        layout.addWidget(captcha_label)
        
        self.captcha_input = QLineEdit()
        layout.addWidget(self.captcha_input)
        
        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def accept(self):
        if self.categories:
            self.category_ids = self.id_input.text().strip()
        self.captcha_text = self.captcha_input.text().strip()
        super().accept()

# 定义一个全局函数，用于替换input函数
original_input = input

def gui_input(prompt):
    """用GUI对话框替代命令行输入"""
    if "分类ID" in prompt:
        # 这个调用是从QuizThread中的一个非主线程调用的，所以我们需要信号和槽
        # 但由于这里无法直接使用，我们返回一个默认值，实际处理会在线程中完成
        return "waiting_for_categories"
    elif "验证码" in prompt:
        # 同上，返回一个默认值
        return "waiting_for_captcha"
    else:
        # 对于其他输入，保持原样
        return original_input(prompt)

# 答题线程类
class QuizThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    captcha_signal = pyqtSignal(str, list)
    
    def __init__(self):
        super().__init__()
        self.quiz_session = QuizSession()
        self.stopped = False
        self.captcha_result = None
        self.categories_result = None
        self.captcha_wait_event = threading.Event()
    
    def run(self):
        try:
            # 保存原始输入函数
            global input
            original_input_func = input
            
            # 从正确的模块导入函数
            from client.senior import captcha_get, captcha_submit, category_get
            
            # 重写输入函数
            def custom_input(prompt):
                if "分类ID" in prompt and hasattr(self, "categories_data"):
                    # 重置等待事件
                    self.captcha_wait_event.clear()
                    # 发出信号请求分类ID
                    self.captcha_signal.emit("", self.categories_data)
                    # 等待结果
                    self.captcha_wait_event.wait(30)  # 最多等待30秒
                    if self.stopped:
                        return ""
                    result = self.categories_result
                    self.categories_result = None
                    return result if result else ""
                elif "验证码" in prompt and hasattr(self, "captcha_url"):
                    # 重置等待事件
                    self.captcha_wait_event.clear()
                    # 发出信号请求验证码
                    self.captcha_signal.emit(self.captcha_url, [])
                    # 等待结果
                    self.captcha_wait_event.wait(30)  # 最多等待30秒
                    if self.stopped:
                        return ""
                    result = self.captcha_result
                    self.captcha_result = None
                    return result if result else ""
                else:
                    self.log_signal.emit(f"输入提示: {prompt}")
                    return original_input_func(prompt)
            
            # 保存原始方法
            original_handle_verification = self.quiz_session.handle_verification
            original_category_get = category_get
            original_captcha_get = captcha_get
            
            # 重写处理验证过程的方法
            def patched_handle_verification():
                try:
                    if self.quiz_session.stopped:
                        self.log_signal.emit("答题已停止")
                        return False
                    
                    self.log_signal.emit("获取分类信息...")
                    category_result = original_category_get()
                    if not category_result:
                        return False
                    
                    if self.quiz_session.stopped:
                        self.log_signal.emit("答题已停止")
                        return False
                    
                    # 保存分类数据供GUI使用
                    self.categories_data = category_result.get('categories', [])
                    self.log_signal.emit("显示验证码分类选择对话框...")
                    
                    # 获取用户输入的分类ID
                    ids = custom_input('请输入分类ID: ')
                    
                    if self.quiz_session.stopped:
                        self.log_signal.emit("答题已停止")
                        return False
                    
                    self.log_signal.emit("获取验证码...")
                    captcha_res = original_captcha_get()
                    if not captcha_res:
                        return False
                    
                    # 保存验证码URL供GUI使用
                    self.captcha_url = captcha_res.get('url')
                    self.log_signal.emit(f"显示验证码输入对话框，验证码链接: {self.captcha_url}")
                    
                    # 获取用户输入的验证码
                    captcha = custom_input('请输入验证码: ')
                    
                    if captcha_submit(code=captcha, captcha_token=captcha_res.get('token'), ids=ids):
                        self.log_signal.emit("验证通过✅")
                        return self.quiz_session.get_question()
                    else:
                        self.log_signal.emit("验证失败")
                        return False
                except Exception as e:
                    self.log_signal.emit(f"验证过程发生错误: {str(e)}")
                    return False
            
            # 应用补丁
            input = custom_input
            self.quiz_session.handle_verification = patched_handle_verification
            
            # 重定向日志输出
            def patched_info(msg, *args, **kwargs):
                self.log_signal.emit(f"INFO: {msg}")
                logger.orig_info(msg, *args, **kwargs)
            
            def patched_error(msg, *args, **kwargs):
                self.log_signal.emit(f"ERROR: {msg}")
                logger.orig_error(msg, *args, **kwargs)
            
            def patched_warning(msg, *args, **kwargs):
                self.log_signal.emit(f"WARNING: {msg}")
                logger.orig_warning(msg, *args, **kwargs)
            
            # 保存原始方法
            if not hasattr(logger, 'orig_info'):
                logger.orig_info = logger.info
                logger.orig_error = logger.error
                logger.orig_warning = logger.warning
            
            # 应用日志补丁
            logger.info = patched_info
            logger.error = patched_error
            logger.warning = patched_warning
            
            # 开始答题
            self.quiz_session.start()
        except Exception as e:
            self.log_signal.emit(f"答题过程出错: {str(e)}")
        finally:
            # 恢复原始方法
            input = original_input_func
            logger.info = logger.orig_info
            logger.error = logger.orig_error
            logger.warning = logger.orig_warning
            self.quiz_session.handle_verification = original_handle_verification
            self.finished_signal.emit()
    
    def stop(self):
        self.stopped = True
        self.quiz_session.stopped = True
        # 防止线程卡在等待输入
        self.captcha_result = ""
        self.categories_result = ""
        self.captcha_wait_event.set()  # 解除等待状态
        self.terminate()
    
    def set_captcha_result(self, captcha_text, category_ids=""):
        self.captcha_result = captcha_text
        if category_ids:
            self.categories_result = category_ids
        # 设置事件，通知等待的线程继续执行
        self.captcha_wait_event.set()

# 主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.quiz_thread = None
        self.current_model_type = "deepseek"  # 默认模型
    
    def initUI(self):
        # 设置窗口属性
        self.setWindowTitle("B站答题助手")
        self.setMinimumSize(800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # 创建各个标签页
        self.setup_home_tab(tab_widget)
        self.setup_settings_tab(tab_widget)
        self.setup_about_tab(tab_widget)
        
        # 初始加载设置
        self.load_settings()
    
    def setup_home_tab(self, tab_widget):
        home_widget = QWidget()
        home_layout = QVBoxLayout(home_widget)
        
        # 顶部状态区域
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.Shape.StyledPanel)
        status_layout = QHBoxLayout(status_frame)
        
        # 登录状态
        self.login_status_label = QLabel("登录状态：未登录")
        login_button = QPushButton("登录B站")
        login_button.clicked.connect(self.login)
        
        # 添加切换账号按钮
        switch_account_button = QPushButton("切换账号")
        switch_account_button.clicked.connect(self.switch_account)
        
        status_layout.addWidget(self.login_status_label)
        status_layout.addStretch()
        status_layout.addWidget(login_button)
        status_layout.addWidget(switch_account_button)
        
        home_layout.addWidget(status_frame)
        
        # 答题控制区域
        control_frame = QFrame()
        control_frame.setFrameShape(QFrame.Shape.StyledPanel)
        control_layout = QHBoxLayout(control_frame)
        
        start_button = QPushButton("开始答题")
        start_button.clicked.connect(self.start_quiz)
        
        stop_button = QPushButton("停止答题")
        stop_button.clicked.connect(self.stop_quiz)
        
        control_layout.addWidget(start_button)
        control_layout.addWidget(stop_button)
        
        home_layout.addWidget(control_frame)
        
        # 日志输出区域
        log_label = QLabel("答题日志:")
        home_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setObjectName("log_text")  # 设置对象名以应用特定样式
        self.log_text.setReadOnly(True)
        home_layout.addWidget(self.log_text)
        
        tab_widget.addTab(home_widget, "首页")
    
    def setup_settings_tab(self, tab_widget):
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        # 模型选择区域
        model_frame = QFrame()
        model_frame.setFrameShape(QFrame.Shape.StyledPanel)
        model_layout = QVBoxLayout(model_frame)
        
        model_layout.addWidget(QLabel("选择AI模型:"))
        
        self.model_combo = QComboBox()
        self.model_combo.addItem("DeepSeek", "deepseek")
        self.model_combo.addItem("Gemini", "gemini")
        self.model_combo.addItem("自定义模型", "custom")
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        
        model_layout.addWidget(self.model_combo)
        
        # 模型配置堆叠部件
        self.model_stack = QStackedWidget()
        
        # DeepSeek配置
        deepseek_widget = QWidget()
        deepseek_layout = QVBoxLayout(deepseek_widget)
        
        deepseek_layout.addWidget(QLabel("DeepSeek API Key:"))
        self.deepseek_key_input = QLineEdit()
        self.deepseek_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        deepseek_layout.addWidget(self.deepseek_key_input)
        
        deepseek_layout.addWidget(QLabel("API 基础URL:"))
        self.deepseek_url_input = QLineEdit()
        deepseek_layout.addWidget(self.deepseek_url_input)
        
        deepseek_layout.addWidget(QLabel("模型名称:"))
        self.deepseek_model_input = QLineEdit()
        deepseek_layout.addWidget(self.deepseek_model_input)
        
        deepseek_save_btn = QPushButton("保存DeepSeek设置")
        deepseek_save_btn.clicked.connect(lambda: self.save_model_settings("deepseek"))
        deepseek_layout.addWidget(deepseek_save_btn)
        
        deepseek_layout.addStretch()
        self.model_stack.addWidget(deepseek_widget)
        
        # Gemini配置
        gemini_widget = QWidget()
        gemini_layout = QVBoxLayout(gemini_widget)
        
        gemini_layout.addWidget(QLabel("Gemini API Key:"))
        self.gemini_key_input = QLineEdit()
        self.gemini_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        gemini_layout.addWidget(self.gemini_key_input)
        
        gemini_layout.addWidget(QLabel("API 基础URL:"))
        self.gemini_url_input = QLineEdit()
        gemini_layout.addWidget(self.gemini_url_input)
        
        gemini_layout.addWidget(QLabel("模型名称:"))
        self.gemini_model_input = QLineEdit()
        gemini_layout.addWidget(self.gemini_model_input)
        
        gemini_save_btn = QPushButton("保存Gemini设置")
        gemini_save_btn.clicked.connect(lambda: self.save_model_settings("gemini"))
        gemini_layout.addWidget(gemini_save_btn)
        
        gemini_layout.addStretch()
        self.model_stack.addWidget(gemini_widget)
        
        # 自定义模型配置
        custom_widget = QWidget()
        custom_layout = QVBoxLayout(custom_widget)
        
        custom_layout.addWidget(QLabel("自定义 API Key:"))
        self.custom_key_input = QLineEdit()
        self.custom_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        custom_layout.addWidget(self.custom_key_input)
        
        custom_layout.addWidget(QLabel("API 基础URL:"))
        self.custom_url_input = QLineEdit()
        custom_layout.addWidget(self.custom_url_input)
        
        custom_layout.addWidget(QLabel("模型名称:"))
        self.custom_model_input = QLineEdit()
        custom_layout.addWidget(self.custom_model_input)
        
        custom_save_btn = QPushButton("保存自定义模型设置")
        custom_save_btn.clicked.connect(lambda: self.save_model_settings("custom"))
        custom_layout.addWidget(custom_save_btn)
        
        # 阿里云配置提示
        tips_label = QLabel("阿里云DashScope提示:\n基础URL: https://dashscope.aliyuncs.com\n模型: qwen-turbo, qwen-plus 或 llama3-8b-chat")
        tips_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        custom_layout.addWidget(tips_label)
        
        custom_layout.addStretch()
        self.model_stack.addWidget(custom_widget)
        
        model_layout.addWidget(self.model_stack)
        settings_layout.addWidget(model_frame)
        
        tab_widget.addTab(settings_widget, "设置")
    
    def setup_about_tab(self, tab_widget):
        about_widget = QWidget()
        about_layout = QVBoxLayout(about_widget)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml("""
        <h2 style="text-align: center;">B站答题助手</h2>
        <p style="text-align: center;">一个帮助B站用户自动完成答题任务的工具</p>
        <p><b>功能特点:</b></p>
        <ul>
            <li>支持使用多种AI模型</li>
            <li>支持DeepSeek、Gemini和自定义模型</li>
            <li>支持阿里云通义千问等API</li>
            <li>现代化GUI界面</li>
        </ul>
        <p><b>使用说明:</b></p>
        <ol>
            <li>在"设置"标签页配置API密钥和模型</li>
            <li>在"首页"登录B站账号</li>
            <li>点击"开始答题"按钮开始自动答题</li>
        </ol>
        <p><b>注意事项:</b></p>
        <ul>
            <li>使用前请确保已配置正确的API密钥</li>
            <li>程序仅调用B站接口和LLM API，不会上传个人信息</li>
            <li>如果使用Gemini，注意需要切换至Gemini允许的地区运行</li>
        </ul>
        """)
        
        about_layout.addWidget(about_text)
        tab_widget.addTab(about_widget, "关于")
    
    def load_settings(self):
        # 加载并检查登录状态
        if is_login():
            self.login_status_label.setText("登录状态：已登录")
        
        # 加载DeepSeek设置
        deepseek_config = load_model_config('deepseek')
        deepseek_key = load_api_key('deepseek')
        self.deepseek_url_input.setText(deepseek_config['base_url'])
        self.deepseek_model_input.setText(deepseek_config['model'])
        self.deepseek_key_input.setText(deepseek_key)
        
        # 加载Gemini设置
        gemini_config = load_model_config('gemini')
        gemini_key = load_api_key('gemini')
        self.gemini_url_input.setText(gemini_config['base_url'])
        self.gemini_model_input.setText(gemini_config['model'])
        self.gemini_key_input.setText(gemini_key)
        
        # 加载自定义模型设置
        custom_config = load_model_config('custom')
        custom_key = load_api_key('custom')
        self.custom_url_input.setText(custom_config['base_url'])
        self.custom_model_input.setText(custom_config['model'])
        self.custom_key_input.setText(custom_key)
    
    def on_model_changed(self, index):
        model_data = self.model_combo.itemData(index)
        self.current_model_type = model_data
        self.model_stack.setCurrentIndex(index)
    
    def save_model_settings(self, model_type):
        if model_type == "deepseek":
            api_key = self.deepseek_key_input.text().strip()
            base_url = self.deepseek_url_input.text().strip()
            model_name = self.deepseek_model_input.text().strip()
        elif model_type == "gemini":
            api_key = self.gemini_key_input.text().strip()
            base_url = self.gemini_url_input.text().strip()
            model_name = self.gemini_model_input.text().strip()
        elif model_type == "custom":
            api_key = self.custom_key_input.text().strip()
            base_url = self.custom_url_input.text().strip()
            model_name = self.custom_model_input.text().strip()
        else:
            return
        
        # 保存API密钥
        if api_key:
            save_api_key(model_type, api_key)
        
        # 保存模型配置
        if base_url and model_name:
            save_model_config(model_type, base_url, model_name)
        
        QMessageBox.information(self, "保存成功", f"{model_type.upper()} 设置已保存")
    
    def login(self):
        # 禁用按钮防止重复点击
        sender = self.sender()
        sender.setEnabled(False)
        
        # 添加登录日志
        self.log_text.append("正在准备B站登录...")
        
        # 创建并显示二维码对话框
        qr_dialog = QRCodeDialog(self)
        
        # 创建登录线程类，避免直接使用threading.Thread
        class LoginThread(QThread):
            finished = pyqtSignal(bool)
            update_qr = pyqtSignal(str)
            
            def run(self):
                try:
                    # 定义GUI回调函数，用于显示二维码
                    def show_qrcode(url):
                        self.update_qr.emit(url)
                    
                    # 调用auth函数，使用GUI模式
                    result = auth(gui_mode=True, gui_callback=show_qrcode)
                    self.finished.emit(result)
                except Exception as e:
                    logger.error(f"登录出错: {str(e)}")
                    self.finished.emit(False)
        
        # 创建线程
        login_thread = LoginThread()
        
        # 连接信号
        login_thread.update_qr.connect(lambda url: qr_dialog.set_qr_code(url))
        login_thread.finished.connect(lambda result: self._on_login_finished(result, qr_dialog, sender))
        
        # 启动线程
        login_thread.start()
        
        # 显示对话框
        qr_dialog.exec()  # 使用exec而不是show，会阻塞直到对话框关闭
    
    def _on_login_finished(self, result, dialog, button):
        """登录完成后的回调"""
        # 更新UI
        if result and is_login():
            self.login_status_label.setText("登录状态：已登录")
            self.log_text.append("登录成功")
            dialog.accept()
        else:
            self.log_text.append("登录失败，请重试")
            dialog.reject()
        
        # 恢复按钮状态
        button.setEnabled(True)
    
    def start_quiz(self):
        # 检查是否已登录
        if not is_login():
            QMessageBox.warning(self, "未登录", "请先登录B站账号")
            return
        
        # 检查当前选择的模型
        model_type = self.current_model_type
        api_key = ""
        
        if model_type == "deepseek":
            api_key = self.deepseek_key_input.text().strip()
            self.model_choice_value = "1"
        elif model_type == "gemini":
            api_key = self.gemini_key_input.text().strip()
            self.model_choice_value = "2"
        elif model_type == "custom":
            api_key = self.custom_key_input.text().strip()
            self.model_choice_value = "3"
        
        if not api_key:
            QMessageBox.warning(self, "API密钥缺失", f"请先在设置中配置{model_type.upper()} API密钥")
            return
        
        # 设置全局模型选择
        import config.config
        config.config.model_choice = self.model_choice_value
        
        # 清空日志
        self.log_text.clear()
        
        # 创建并启动答题线程
        if self.quiz_thread is not None and self.quiz_thread.isRunning():
            self.stop_quiz()
        
        self.quiz_thread = QuizThread()
        self.quiz_thread.log_signal.connect(self.update_log)
        self.quiz_thread.finished_signal.connect(self.on_quiz_finished)
        self.quiz_thread.captcha_signal.connect(self.show_captcha_dialog)
        
        # 设置线程中QuizSession的模型选择
        self.quiz_thread.quiz_session.update_model_choice(self.model_choice_value)
        
        self.quiz_thread.start()
        
        self.log_text.append(f"开始使用 {model_type.upper()} 模型答题...")
        
        # 禁用开始按钮
        self.sender().setEnabled(False)
    
    def stop_quiz(self):
        if self.quiz_thread is not None and self.quiz_thread.isRunning():
            self.quiz_thread.stop()
            self.log_text.append("正在停止答题...")
    
    def on_quiz_finished(self):
        # 恢复开始按钮
        for button in self.findChildren(QPushButton):
            if button.text() == "开始答题":
                button.setEnabled(True)
        
        self.log_text.append("答题已结束")
    
    def update_log(self, text):
        self.log_text.append(text)
        # 自动滚动到底部
        self.log_text.moveCursor(QTextCursor.MoveOperation.End)
    
    def show_captcha_dialog(self, url, categories):
        """在主线程中显示验证码对话框"""
        dialog = CaptchaDialog(url, categories, self)
        if dialog.exec():
            if categories:
                self.quiz_thread.set_captcha_result(dialog.captcha_text, dialog.category_ids)
            else:
                self.quiz_thread.set_captcha_result(dialog.captcha_text)
        else:
            # 用户取消了对话框，停止答题
            self.stop_quiz()
    
    def switch_account(self):
        """切换账号功能，先登出当前账号，然后进行重新登录"""
        # 添加日志
        self.log_text.append("正在切换账号...")
        
        # 禁用按钮防止重复点击
        sender = self.sender()
        sender.setEnabled(False)
        
        # 创建并显示二维码对话框
        qr_dialog = QRCodeDialog(self)
        
        # 创建切换账号线程类
        class SwitchAccountThread(QThread):
            finished = pyqtSignal(bool)
            update_qr = pyqtSignal(str)
            logout_signal = pyqtSignal(bool)
            
            def run(self):
                try:
                    # 先登出当前账号
                    logout_result = logout()
                    self.logout_signal.emit(logout_result)
                    
                    if logout_result:
                        # 定义GUI回调函数，用于显示二维码
                        def show_qrcode(url):
                            self.update_qr.emit(url)
                        
                        # 调用登录函数
                        result = auth(gui_mode=True, gui_callback=show_qrcode)
                        self.finished.emit(result)
                    else:
                        self.finished.emit(False)
                except Exception as e:
                    logger.error(f"切换账号过程出错: {str(e)}")
                    self.finished.emit(False)
        
        # 创建线程
        switch_thread = SwitchAccountThread()
        
        # 连接信号
        switch_thread.logout_signal.connect(lambda result: 
            self.log_text.append("已登出当前账号" if result else "登出失败，无法切换账号"))
        switch_thread.update_qr.connect(lambda url: qr_dialog.set_qr_code(url))
        switch_thread.finished.connect(lambda result: self._on_switch_account_finished(result, qr_dialog, sender))
        
        # 启动线程
        switch_thread.start()
        
        # 显示对话框
        qr_dialog.exec()
    
    def _on_switch_account_finished(self, result, dialog, button):
        """切换账号完成后的回调"""
        # 更新UI
        if result and is_login():
            self.login_status_label.setText("登录状态：已登录")
            self.log_text.append("新账号登录成功")
            dialog.accept()
        else:
            if not dialog.login_result:  # 避免重复显示错误消息
                self.log_text.append("登录失败，请重试")
            dialog.reject()
        
        # 恢复按钮状态
        button.setEnabled(True)

# 主程序入口
def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE_SHEET)
    
    # 加载默认模型设置，但不要求用户立即选择模型
    # 用户可以在GUI界面中选择模型
    from config.config import model_choice, API_KEY_GEMINI, API_KEY_DEEPSEEK, API_KEY_CUSTOM, CUSTOM_MODEL_CONFIG
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 