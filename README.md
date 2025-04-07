# bilibili-AIHardcore

B 站硬核会员自动答题工具，利用 LLM 实现智能答题功能。
**可用的模型：**
- OpenAI API兼容的其他 API（火山引擎、硅基流动等）

![Image](https://github.com/user-attachments/assets/ad523686-ec27-4566-8b43-7dac6efa0579)

![Image](https://github.com/user-attachments/assets/0a93b6bb-4266-4317-a7a3-ef56333949d0)


⚠️请避免使用思考模型，防止超时报错
## 使用说明

1. 克隆项目到本地

```bash
git clone [项目地址]
cd bilibili-AIHardcore
```

2. 安装依赖

```bash
pip install -r requirements.txt
```
3. 运行主程序

```bash
python gui_main.py
```
## 使用流程
1. 选择回答模型
2. 输入自己的 API Key
3. 扫描二维码登录
4. 输入要进行答题的分类
5. 查看并输入图形验证码
6. 程序会自动开始答题流程

## 常见问题
1. 二维码乱码：请尝试在 Windows Terminal 中使用命令运行 exe，或手动生成二维码进行扫码
2. 答题不及格：尝试使用历史分区答题，历史分区的准确率较高
3. AI 卡在一个问题一直过不去，回复类似于“无法确认、我不清楚”：去 B 站 APP 手动把卡住的题目过了，切记不要在 B 站答题页面点击左上角返回按钮退出，会结束答题

## Gemini 模型使用问题及解决办法
1. 答题触发 429 错误：应该是触发了 Gemini 每分钟调用限制或触发了风控，依次尝试以下操作：
    1. 可以稍等一下重新运行，会接着中断的题目继续回答
    2. 如果还不行，尝试切换节点（修改IP）
    3. 再不行就需要手动修改一下代码里的 prompt
    4. 终极解决办法：别用 Gemini 模型了，用 DeepSeek 模型
2. 开始答题直接之后软件直接退出：需要切换到大陆及香港以外的节点进行答题

## 注意事项
- 使用前请确保已配置正确的 API Key
- 程序仅调用 B 站接口和 LLM API，不会上传任何个人信息
- 首次输入 API Key 和登录后，会将信息保存到 `~/.bilibili-AIHardcore`，下次运行时会自动读取。如遇到奇怪问题，请先清空此文件夹重新运行软件
- 如果使用Gemini，注意需要切换至 Gemini 允许的地区运行，否则会被 Gemini API 拦截
- 请合理使用，遵守 B 站相关规则
