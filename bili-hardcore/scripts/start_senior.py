from client.senior import captcha_get, captcha_submit, category_get, question_get, question_submit
from tools.logger import logger
from tools.LLM.gemini import GeminiAPI
from tools.LLM.deepseek import DeepSeekAPI
from tools.LLM.custom import CustomAPI
from config.config import model_choice
from time import sleep

class QuizSession:
    def __init__(self):
        self.question_id = None
        self.answers = None
        self.question_num = 0
        self.question = None
        self.stopped = False
        # 从配置中获取当前选择的模型
        self.current_model = model_choice

    def start(self):
        """开始答题会话"""
        try:
            while self.question_num < 100 and not self.stopped:
                if not self.get_question():
                    logger.error("获取题目失败")
                    return
                
                # 检查是否停止
                if self.stopped:
                    logger.info("答题已停止")
                    return
                
                # 显示题目信息
                self.display_question()
                # 根据用户选择初始化对应的LLM模型
                # 使用类中缓存的当前模型选择，这样可以随时更新
                if self.current_model == '1':
                    llm = DeepSeekAPI()
                elif self.current_model == '2':
                    llm = GeminiAPI()
                elif self.current_model == '3':
                    llm = CustomAPI()
                else:
                    llm = DeepSeekAPI()
                
                # 检查是否停止
                if self.stopped:
                    logger.info("答题已停止")
                    return
                    
                answer = llm.ask(self.get_question_prompt())
                logger.info('AI给出的答案:{}'.format(answer))
                
                # 检查是否停止
                if self.stopped:
                    logger.info("答题已停止")
                    return
                
                try:
                    answer = int(answer)
                    if not (1 <= answer <= len(self.answers)):
                        logger.warning(f"无效的答案序号: {answer}")
                        continue
                except ValueError:
                    logger.warning("AI回复其他内容,正在重试")
                    continue

                result = self.answers[answer-1]
                
                # 检查是否停止
                if self.stopped:
                    logger.info("答题已停止")
                    return
                
                if not self.submit_answer(result):
                    logger.error("提交答案失败")
                    return
        except KeyboardInterrupt:
            logger.info("答题会话已终止")
        except Exception as e:
            logger.error(f"答题过程发生错误: {str(e)}")
    
    # 允许外部更新当前使用的模型
    def update_model_choice(self, new_model_choice):
        """更新当前使用的模型
        
        Args:
            new_model_choice (str): 新的模型选择 ('1', '2' 或 '3')
        """
        self.current_model = new_model_choice
        logger.info(f"已更新模型选择为: {self.current_model}")

    def get_question(self):
        """获取题目
        
        Returns:
            bool: 是否成功获取题目
        """
        try:
            question = question_get()
            if not question:
                return False

            if question.get('code') != 0:
                logger.info("需要验证码验证")
                return self.handle_verification()

            data = question.get('data', {})
            self.question = data.get('question')
            self.answers = data.get('answers', [])
            self.question_id = data.get('id')
            self.question_num = data.get('question_num', 0)
            return True

        except Exception as e:
            logger.error(f"获取题目失败: {str(e)}")
            return False

    def handle_verification(self):
        """处理验证码验证
        
        Returns:
            bool: 验证是否成功
        """
        try:
            # 检查是否停止
            if self.stopped:
                logger.info("答题已停止")
                return False
                
            logger.info("获取分类信息...")
            category = category_get()
            if not category:
                return False
            
            # 检查是否停止
            if self.stopped:
                logger.info("答题已停止")
                return False
                
            logger.info("分类信息:")
            for cat in category.get('categories', []):
                logger.info(f"ID: {cat.get('id')} - {cat.get('name')}")
            logger.info("tips: 输入多个分类ID请用 *英文逗号* 隔开,例如:1,2,3")
            ids = input('请输入分类ID: ')
            
            # 检查是否停止
            if self.stopped:
                logger.info("答题已停止")
                return False
                
            logger.info("获取验证码...")
            captcha_res = captcha_get()
            logger.info("请打开链接查看验证码内容:{}".format(captcha_res.get('url')))
            if not captcha_res:
                return False
                
            # 检查是否停止
            if self.stopped:
                logger.info("答题已停止")
                return False
                
            captcha = input('请输入验证码: ')

            if captcha_submit(code=captcha, captcha_token=captcha_res.get('token'), ids=ids):
                logger.info("验证通过✅")
                return self.get_question()
            else:
                logger.error("验证失败")
                return False

        except Exception as e:
            logger.error(f"验证过程发生错误: {str(e)}")
            return False

    def display_question(self):
        """显示当前题目和选项"""
        if not self.answers:
            logger.warning("没有可用的题目")
            return

        logger.info(f"第{self.question_num}题:{self.question}")
        for i, answer in enumerate(self.answers, 1):
            logger.info(f"{i}. {answer.get('ans_text')}")
    
    def get_question_prompt(self):
        return '''
        题目:{}
        答案:{}
        '''.format(self.question, self.answers)

    def submit_answer(self, answer):
        """提交答案
        
        Args:
            answer (dict): 答案信息
        
        Returns:
            bool: 是否成功提交答案
        """
        try:
            result = question_submit(
                self.question_id,
                answer.get('ans_hash'),
                answer.get('ans_text')
            )
            if result and result.get('code') == 0:
                logger.info("答案提交成功")
                sleep(1)
                return True
            else:
                logger.error(f"答案提交失败: {result}")
                return False
        except Exception as e:
            logger.error(f"提交答案时发生错误: {str(e)}")
            return False

# 创建答题会话实例
quiz_session = QuizSession()

def start():
    """启动答题程序"""
    quiz_session.start()
    logger.info('答题结束')