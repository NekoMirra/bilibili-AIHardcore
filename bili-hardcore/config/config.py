import os

# API Keys
import json

<<<<<<< HEAD
# Model configurations - base URLs and default models
MODEL_CONFIGS = {
    'deepseek': {
        'base_url': 'https://api.deepseek.com/v1',
        'model': 'deepseek-chat'
    },
    'gemini': {
        'base_url': 'https://generativelanguage.googleapis.com/v1beta',
        'model': 'gemini-2.0-flash'
    },
    'custom': {
        'base_url': '',
        'model': ''
    },
    # 阿里云DashScope模型配置示例
    'dashscope': {
        'base_url': 'https://dashscope.aliyuncs.com',
        'model': 'qwen-turbo'  # 可选：qwen-turbo, qwen-plus, llama3-8b-chat等
    }
}

def load_model_config(model_type):
    """从用户目录加载模型配置
    
    Args:
        model_type (str): 模型类型 (gemini, deepseek, 或 custom)
    
    Returns:
        dict: 模型配置信息，包含 base_url 和 model
    """
    config_file = os.path.join(os.path.expanduser('~'), '.bili-hardcore', f'{model_type}_config.json')
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                if data:
                    return {
                        'base_url': data.get('base_url', MODEL_CONFIGS[model_type]['base_url']),
                        'model': data.get('model', MODEL_CONFIGS[model_type]['model'])
                    }
        except Exception as e:
            print(f'读取{model_type.upper()}模型配置失败: {str(e)}')
    return MODEL_CONFIGS[model_type].copy()

def save_model_config(model_type, base_url, model_name):
    """保存模型配置到用户目录
    
    Args:
        model_type (str): 模型类型 (gemini, deepseek, 或 custom)
        base_url (str): API的基础URL
        model_name (str): 模型名称
    """
    config_file = os.path.join(os.path.expanduser('~'), '.bili-hardcore', f'{model_type}_config.json')
    try:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump({
                'base_url': base_url,
                'model': model_name
            }, f)
        print(f'{model_type.upper()}模型配置已保存')
    except Exception as e:
        print(f'保存{model_type.upper()}模型配置失败: {str(e)}')
=======
# OpenAI默认配置
BASE_URL_OPENAI = ''
MODEL_OPENAI = ''
API_KEY_OPENAI = ''
>>>>>>> bc4dce083e196db131ba6d615dc44efa150e2dee

def load_api_key(key_type):
    """从用户目录加载API密钥
    
    Args:
        key_type (str): API类型 (gemini 或 deepseek)
    
    Returns:
        str: API密钥
    """
    key_file = os.path.join(os.path.expanduser('~'), '.bili-hardcore', f'{key_type}_key.json')
    if os.path.exists(key_file):
        try:
            with open(key_file, 'r') as f:
                data = json.load(f)
                return data.get('api_key', '')
        except Exception as e:
            print(f'读取{key_type.upper()} API密钥失败: {str(e)}')
    return ''

def save_api_key(key_type, api_key):
    """保存API密钥到用户目录
    
    Args:
        key_type (str): API类型 (gemini 或 deepseek)
        api_key (str): API密钥
    """
    key_file = os.path.join(os.path.expanduser('~'), '.bili-hardcore', f'{key_type}_key.json')
    try:
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        with open(key_file, 'w') as f:
            json.dump({'api_key': api_key}, f)
        print(f'{key_type.upper()} API密钥已保存')
    except Exception as e:
        print(f'保存{key_type.upper()} API密钥失败: {str(e)}')

# 从用户目录加载API密钥，如果不存在则提示用户输入
def load_gemini_key():
    """从用户目录加载GEMINI API密钥
    
    Returns:
        str: API密钥
    """
    key_file = os.path.join(os.path.expanduser('~'), '.bili-hardcore', 'gemini_key.json')
    if os.path.exists(key_file):
        try:
            with open(key_file, 'r') as f:
                data = json.load(f)
                return data.get('api_key', '')
        except Exception as e:
            print(f'读取GEMINI API密钥失败: {str(e)}')
    return ''

def save_gemini_key(api_key):
    save_api_key('gemini', api_key)

<<<<<<< HEAD
def init_model_settings():
    """初始化模型设置，由用户选择模型并设置API密钥
    
    Returns:
        tuple: (model_choice, API_KEY_GEMINI, API_KEY_DEEPSEEK, API_KEY_CUSTOM, CUSTOM_MODEL_CONFIG)
    """
    print("请选择使用的LLM模型：")
    print("1. DeepSeek")
    print("2. Gemini")
    print("3. 自定义模型")
    model_choice = input("请输入数字(1、2或3): ").strip()
    
    API_KEY_GEMINI = ''
    API_KEY_DEEPSEEK = ''
    API_KEY_CUSTOM = ''
    CUSTOM_MODEL_CONFIG = None
    
    if model_choice == '2':
        # 加载Gemini模型配置
        gemini_config = load_model_config('gemini')
        
        # 加载API Key
        API_KEY_GEMINI = load_api_key('gemini')
        if not API_KEY_GEMINI:
            API_KEY_GEMINI = input('请输入GEMINI API密钥: ').strip()
            if API_KEY_GEMINI:
                save_api_key('gemini', API_KEY_GEMINI)
    
    elif model_choice == '1':
        # 加载DeepSeek模型配置
        deepseek_config = load_model_config('deepseek')
        
        # 加载API Key
        API_KEY_DEEPSEEK = load_api_key('deepseek')
        if not API_KEY_DEEPSEEK:
            API_KEY_DEEPSEEK = input('请输入DEEPSEEK API密钥: ').strip()
            if API_KEY_DEEPSEEK:
                save_api_key('deepseek', API_KEY_DEEPSEEK)
    elif model_choice == '3':
        # 加载自定义模型配置
        custom_config = load_model_config('custom')
        
        # 如果没有配置过或需要修改配置
        if not custom_config['base_url'] or input('是否需要修改自定义模型配置？(y/n): ').lower() == 'y':
            print("\n=== 自定义模型配置 ===")
            print("提示: 对于阿里云模型，请使用 https://dashscope.aliyuncs.com 作为基础URL")
            print("常用模型名称示例:")
            print("- 阿里云通义千问: qwen-turbo, qwen-plus, llama3-8b-chat")
            print("- OpenAI兼容API: gpt-3.5-turbo, gpt-4-turbo等")
            print("=========\n")
            
            custom_config['base_url'] = input('请输入自定义模型API基础URL (例如: https://api.example.com/v1): ').strip()
            custom_config['model'] = input('请输入自定义模型名称: ').strip()
            save_model_config('custom', custom_config['base_url'], custom_config['model'])
        
        # 加载API Key
        API_KEY_CUSTOM = load_api_key('custom')
        if not API_KEY_CUSTOM:
            API_KEY_CUSTOM = input('请输入自定义模型API密钥: ').strip()
            if API_KEY_CUSTOM:
                save_api_key('custom', API_KEY_CUSTOM)
        
        CUSTOM_MODEL_CONFIG = custom_config
    else:
        print("无效的选择，默认使用deepseek")
        # 加载DeepSeek模型配置
        deepseek_config = load_model_config('deepseek')
        
        # 加载API Key
        API_KEY_DEEPSEEK = load_api_key('deepseek')
        if not API_KEY_DEEPSEEK:
            API_KEY_DEEPSEEK = input('请输入DEEPSEEK API密钥: ').strip()
            if API_KEY_DEEPSEEK:
                save_api_key('deepseek', API_KEY_DEEPSEEK)
                
    return model_choice, API_KEY_GEMINI, API_KEY_DEEPSEEK, API_KEY_CUSTOM, CUSTOM_MODEL_CONFIG

# 设置默认值
model_choice = '1'  # 默认使用DeepSeek
API_KEY_GEMINI = load_api_key('gemini')
API_KEY_DEEPSEEK = load_api_key('deepseek')
API_KEY_CUSTOM = load_api_key('custom')
CUSTOM_MODEL_CONFIG = load_model_config('custom')
=======
def save_openai_config(base_url, model, api_key):
    """保存OpenAI配置到用户目录
    
    Args:
        base_url (str): OpenAI API基础URL
        model (str): 模型名称
        api_key (str): API密钥
    """
    config_file = os.path.join(os.path.expanduser('~'), '.bili-hardcore', 'openai_config.json')
    try:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump({
                'base_url': base_url,
                'model': model,
                'api_key': api_key
            }, f)
        print('OpenAI配置已保存')
    except Exception as e:
        print(f'保存OpenAI配置失败: {str(e)}')

def load_openai_config():
    """从用户目录加载OpenAI配置
    
    Returns:
        tuple: (base_url, model, api_key)
    """
    config_file = os.path.join(os.path.expanduser('~'), '.bili-hardcore', 'openai_config.json')
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                return data.get('base_url', ''), data.get('model', ''), data.get('api_key', '')
        except Exception as e:
            print(f'读取OpenAI配置失败: {str(e)}')
    return '', '', ''

# 选择使用的LLM模型
print("请选择使用的LLM模型：")
print("1. DeepSeek")
print("2. Gemini")
print("3. OpenAI 格式的 API（火山引擎、硅基流动等）")
model_choice = input("请输入数字(1,2,3): ").strip()

API_KEY_GEMINI = ''
API_KEY_DEEPSEEK = ''

if model_choice == '2':
    API_KEY_GEMINI = load_api_key('gemini')
    if not API_KEY_GEMINI:
        API_KEY_GEMINI = input('请输入GEMINI API密钥: ').strip()
        if API_KEY_GEMINI:
            save_api_key('gemini', API_KEY_GEMINI)

elif model_choice == '1':
    API_KEY_DEEPSEEK = load_api_key('deepseek')
    if not API_KEY_DEEPSEEK:
        API_KEY_DEEPSEEK = input('请输入DEEPSEEK API密钥: ').strip()
        if API_KEY_DEEPSEEK:
            save_api_key('deepseek', API_KEY_DEEPSEEK)
            
elif model_choice == '3':
    BASE_URL_OPENAI, MODEL_OPENAI, API_KEY_OPENAI = load_openai_config()
    if not all([BASE_URL_OPENAI, MODEL_OPENAI, API_KEY_OPENAI]):
        BASE_URL_OPENAI = input('请输入API基础URL (例如: https://api.openai.com/v1): ').strip()
        if BASE_URL_OPENAI.endswith('/'):
            BASE_URL_OPENAI = BASE_URL_OPENAI.rstrip('/')
        MODEL_OPENAI = input('请输入模型名称 (例如: gpt-3.5-turbo): ').strip()
        API_KEY_OPENAI = input('请输入API密钥: ').strip()
        if all([BASE_URL_OPENAI, MODEL_OPENAI, API_KEY_OPENAI]):
            save_openai_config(BASE_URL_OPENAI, MODEL_OPENAI, API_KEY_OPENAI)
else:
    print("无效的选择，默认使用deepseek")
    API_KEY_DEEPSEEK = load_api_key('deepseek')
    if not API_KEY_DEEPSEEK:
        API_KEY_DEEPSEEK = input('请输入DEEPSEEK API密钥:').strip()
        if API_KEY_DEEPSEEK:
            save_api_key('deepseek', API_KEY_DEEPSEEK)
>>>>>>> bc4dce083e196db131ba6d615dc44efa150e2dee

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志目录
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# API配置
API_CONFIG = {
    'appkey': '783bbb7264451d82',
    'appsec': '2653583c8873dea268ab9386918b1d65',
    'user_agent': 'Mozilla/5.0 BiliDroid/1.12.0 (bbcallen@gmail.com)',
}

# 请求头配置
HEADERS = {
    'User-Agent': API_CONFIG['user_agent'],
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'x-bili-metadata-legal-region': 'CN',
    'x-bili-aurora-eid': '',
    'x-bili-aurora-zone': '',
}

# 认证文件路径
AUTH_FILE = os.path.join(os.path.expanduser('~'), '.bili-hardcore', 'auth.json')

PROMPT = '''
当前时间：{}
你是一个高效精准的答题专家，面对选择题时，直接根据问题和选项判断正确答案，并返回对应选项的序号（1, 2, 3, 4）。示例：
问题：大的反义词是什么？
选项：['长', '宽', '小', '热']
回答：3
如果不确定正确答案，选择最接近的选项序号返回，不提供额外解释或超出 1-4 的内容。
---
请回答我的问题：{}
'''

# 如果是命令行模式（不是被导入），则初始化模型设置
if __name__ == "__main__":
    model_choice, API_KEY_GEMINI, API_KEY_DEEPSEEK, API_KEY_CUSTOM, CUSTOM_MODEL_CONFIG = init_model_settings()