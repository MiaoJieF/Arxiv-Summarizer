from flask import Flask, request, jsonify
from flask_cors import CORS
import arxiv
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
import PyPDF2
import io
import requests
from config import Config

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 验证配置
try:
    Config.validate_config()
except ValueError as e:
    print(f"配置错误: {e}")
    print("请创建.env文件并设置相应的配置")

# 初始化模型
def get_llm():
    """根据配置获取相应的语言模型"""
    if Config.MODEL_TYPE == 'openai':
        return ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=0.7,
            openai_api_key=Config.OPENAI_API_KEY
        )
    elif Config.MODEL_TYPE == 'ollama':
        return ChatOllama(
            model=Config.OLLAMA_MODEL,
            base_url=Config.OLLAMA_BASE_URL,
            temperature=0.7
        )
    else:
        raise ValueError(f"不支持的模型类型: {Config.MODEL_TYPE}")

# 全局模型实例
llm = get_llm()

@app.route('/api/search', methods=['POST'])
def search_papers():
    """搜索arXiv论文"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        sort_by = data.get('sort_by', 'relevance')

        if not query:
            return jsonify({'error': '查询参数不能为空'}), 400
        
        # 根据参数选择排序方式
        if sort_by == 'latest':
            sort_criterion = arxiv.SortCriterion.SubmittedDate
        else:
            sort_criterion = arxiv.SortCriterion.Relevance
        
        # 搜索arXiv论文
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_criterion
        )
        
        papers = []
        for result in search.results():
            paper = {
                'id': result.entry_id,
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'abstract': result.summary,
                'published': result.published.isoformat(),
                'pdf_url': result.pdf_url,
                'categories': result.categories
            }
            papers.append(paper)
        
        return jsonify({'papers': papers})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize_paper():
    """使用LangChain生成论文总结"""
    try:
        data = request.get_json()
        paper_id = data.get('paper_id', '')
        pdf_url = data.get('pdf_url', '')
        abstract = data.get('abstract', '')
        
        if not paper_id or not pdf_url:
            return jsonify({'error': '论文ID和PDF链接不能为空'}), 400
        
        # 尝试下载并解析PDF
        try:
            response = requests.get(pdf_url)
            response.raise_for_status()
            
            # 使用PyPDF2解析PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            # 如果PDF解析失败，使用摘要
            if not text.strip():
                text = abstract
                
        except Exception as e:
            print(f"PDF解析失败: {e}")
            text = abstract
        
        # 使用LangChain生成总结
        system_message = SystemMessage(content="""你是一个专业的学术论文总结助手。请根据提供的论文内容，生成一个结构化的总结，包括：
1. 研究背景和动机
2. 主要方法和创新点
3. 实验结果和发现
4. 结论和意义
5. 关键词

请用中文回答，语言要简洁明了，适合学术阅读。""")
        
        human_message = HumanMessage(content=f"请总结以下论文内容：\n\n{text[:4000]}")  # 限制文本长度
        
        messages = [system_message, human_message]
        response = llm.invoke(messages)
        
        summary = response.content
        
        return jsonify({
            'paper_id': paper_id,
            'summary': summary,
            'source': 'pdf' if text != abstract else 'abstract'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'healthy', 'message': 'arXiv Summarizer API is running'})

@app.route('/api/models', methods=['GET'])
def get_models():
    """获取可用模型列表"""
    return jsonify({
        'current_model_type': Config.MODEL_TYPE,
        'current_model': Config.OPENAI_MODEL if Config.MODEL_TYPE == 'openai' else Config.OLLAMA_MODEL,
        'available_models': Config.get_available_models()
    })

@app.route('/api/model/switch', methods=['POST'])
def switch_model():
    """切换模型类型"""
    try:
        data = request.get_json()
        model_type = data.get('model_type', '')
        model_name = data.get('model_name', '')
        
        if model_type not in ['openai', 'ollama']:
            return jsonify({'error': '模型类型必须是openai或ollama'}), 400
        
        # 更新配置
        Config.MODEL_TYPE = model_type
        if model_type == 'openai':
            Config.OPENAI_MODEL = model_name or 'gpt-3.5-turbo'
        else:
            Config.OLLAMA_MODEL = model_name or 'llama2'
        
        # 重新初始化模型
        global llm
        llm = get_llm()
        
        return jsonify({
            'message': '模型切换成功',
            'model_type': Config.MODEL_TYPE,
            'model_name': Config.OPENAI_MODEL if Config.MODEL_TYPE == 'openai' else Config.OLLAMA_MODEL
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model/test', methods=['POST'])
def test_model():
    """测试当前模型"""
    try:
        # 简单的测试消息
        test_message = HumanMessage(content="请回复'模型测试成功'")
        response = llm.invoke([test_message])
        
        return jsonify({
            'status': 'success',
            'model_type': Config.MODEL_TYPE,
            'model_name': Config.OPENAI_MODEL if Config.MODEL_TYPE == 'openai' else Config.OLLAMA_MODEL,
            'response': response.content
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'model_type': Config.MODEL_TYPE,
            'model_name': Config.OPENAI_MODEL if Config.MODEL_TYPE == 'openai' else Config.OLLAMA_MODEL
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
