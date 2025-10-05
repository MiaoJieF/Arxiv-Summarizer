import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""
    
    # 模型配置
    MODEL_TYPE = os.getenv('MODEL_TYPE', 'openai')  # 'openai' 或 'ollama'
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Ollama配置
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')
    
    # Flask配置
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # 其他配置
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB
    
    @staticmethod
    def validate_config():
        """验证配置是否完整"""
        if Config.MODEL_TYPE == 'openai':
            if not Config.OPENAI_API_KEY:
                raise ValueError("使用OpenAI模型时，请设置OPENAI_API_KEY环境变量")
        elif Config.MODEL_TYPE == 'ollama':
            # Ollama不需要API密钥，只需要确保服务运行
            pass
        else:
            raise ValueError("MODEL_TYPE必须是'openai'或'ollama'")
        return True
    
    @staticmethod
    def get_available_models():
        """获取可用的模型列表"""
        return {
            'openai': [
                'gpt-3.5-turbo',
                'gpt-4',
                'gpt-4-turbo-preview'
            ],
            'ollama': [
                'llama2',
                'llama2:13b',
                'llama2:70b',
                'codellama',
                'mistral',
                'neural-chat',
                'starling-lm',
                'vicuna',
                'wizard-vicuna-uncensored'
            ]
        }
