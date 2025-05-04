import requests
from typing import Dict, Any, Optional
from config.config import PROMPT, API_KEY_CUSTOM, CUSTOM_MODEL_CONFIG, load_model_config
from time import time

class CustomAPI:
    def __init__(self):
        # 如果直接从config中获取的配置为None，则尝试从文件加载
        if CUSTOM_MODEL_CONFIG is None:
            config = load_model_config('custom')
        else:
            config = CUSTOM_MODEL_CONFIG

        self.base_url = config['base_url']
        self.model = config['model']
        self.api_key = API_KEY_CUSTOM

    def ask(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """根据API格式自动判断使用不同的API格式"""
        # 增加更多的OpenAI兼容API识别条件
        if ('openai' in self.base_url.lower() or
            '/chat/completions' in self.base_url.lower() or
            'api.b9349.dpdns.org' in self.base_url.lower() or  # 添加你的特定API域名
            self.base_url.lower().endswith('/v1') or
            self.base_url.lower().endswith('/v1/')):
            return self.ask_openai_format(question, timeout)
        elif 'dashscope' in self.base_url.lower() or 'aliyuncs' in self.base_url.lower():
            return self.ask_dashscope_format(question, timeout)
        else:
            return self.ask_custom_format(question, timeout)

    def ask_openai_format(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """使用OpenAI格式的API调用"""
        # 更灵活的URL处理
        if '/chat/completions' in self.base_url:
            url = f"{self.base_url}"
        elif self.base_url.endswith('/v1') or self.base_url.endswith('/v1/'):
            # 如果URL以/v1或/v1/结尾，直接添加chat/completions
            url = f"{self.base_url.rstrip('/')}/chat/completions"
        else:
            # 否则添加/v1/chat/completions
            url = f"{self.base_url.rstrip('/')}/v1/chat/completions"

        print(f"DEBUG: 使用API URL: {url}")  # 调试信息

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": PROMPT.format(time(), question)
                }
            ]
        }

        try:
            print(f"DEBUG: 发送请求到 {url}，模型: {self.model}")
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=timeout
            )

            # 打印响应状态和内容以便调试
            print(f"DEBUG: 响应状态码: {response.status_code}")
            print(f"DEBUG: 响应内容: {response.text[:200]}...")  # 只打印前200个字符

            response.raise_for_status()

            # 解析JSON响应
            json_response = response.json()
            print(f"DEBUG: JSON响应结构: {list(json_response.keys())}")

            return json_response["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            error_msg = f"自定义模型API请求失败: {str(e)}"
            print(f"ERROR: {error_msg}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"ERROR: 响应状态码: {e.response.status_code}")
                print(f"ERROR: 响应内容: {e.response.text[:500]}")  # 打印更多错误内容
            raise Exception(error_msg)
        except (KeyError, IndexError) as e:
            error_msg = f"解析API响应失败: {str(e)}，请检查模型配置是否正确"
            print(f"ERROR: {error_msg}")
            print(f"ERROR: 可能的响应格式不匹配，请检查API文档")
            raise Exception(error_msg)

    def ask_dashscope_format(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """使用阿里云DashScope API格式的调用"""
        # 确保URL正确指向chat/completions端点
        url = f"{self.base_url}/compatible-mode/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": PROMPT.format(time(), question)
                }
            ]
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"阿里云DashScope API请求失败: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"解析API响应失败: {str(e)}，请检查模型配置是否正确")

    def ask_custom_format(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """使用自定义格式的API调用，适配其他格式的模型API"""
        url = f"{self.base_url}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 通用数据格式，可根据实际API调整
        data = {
            "model": self.model,
            "prompt": PROMPT.format(time(), question)
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()

            # 尝试通用的响应解析，根据实际情况可能需要调整
            result = response.json()
            if "choices" in result and isinstance(result["choices"], list) and len(result["choices"]) > 0:
                if "message" in result["choices"][0]:
                    return result["choices"][0]["message"]["content"]
                elif "text" in result["choices"][0]:
                    return result["choices"][0]["text"]
            elif "response" in result:
                return result["response"]
            elif "content" in result:
                return result["content"]
            elif "answer" in result:
                return result["answer"]
            elif "output" in result:
                return result["output"]
            elif "result" in result:
                return result["result"]
            else:
                # 如果找不到标准格式，返回整个响应，让用户自己查看
                return str(result)
        except requests.exceptions.RequestException as e:
            raise Exception(f"自定义模型API请求失败: {str(e)}")
        except Exception as e:
            raise Exception(f"解析API响应失败: {str(e)}，请检查模型配置是否正确")