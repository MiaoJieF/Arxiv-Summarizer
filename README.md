# arXiv论文搜索与总结工具

一个基于Flask和LangChain的arXiv论文搜索与AI总结工具，提供现代化的Web界面来搜索学术论文并生成智能总结。

![演示视频](assets/video.gif)

## 功能特性

- 🔍 **智能搜索**: 基于关键词搜索arXiv论文库
- 🤖 **AI总结**: 使用LangChain生成论文总结，支持多种大模型
- 📄 **PDF解析**: 自动下载并解析论文PDF内容
- 🎨 **现代UI**: 响应式设计，支持移动端
- ⚡ **实时反馈**: 搜索和总结过程的实时状态更新
- 🔄 **模型切换**: 支持OpenAI API和Ollama本地模型
- 🧪 **模型测试**: 实时测试模型连接和响应

## 项目结构

```
arxiv_summarizer/
├── backend/                 # 后端Flask应用
│   ├── venv/               # Python虚拟环境
│   ├── app.py              # Flask主应用
│   ├── config.py           # 配置管理
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端静态文件
│   ├── index.html          # 主页面
│   ├── style.css           # 样式文件
│   └── script.js           # JavaScript逻辑
└── README.md               # 项目说明
```

## 技术栈

### 后端
- **Flask**: Web框架
- **LangChain**: AI应用框架
- **OpenAI**: 大语言模型API
- **Ollama**: 本地大语言模型
- **arxiv**: arXiv论文库接口
- **PyPDF2**: PDF文档解析

### 前端
- **HTML5**: 页面结构
- **CSS3**: 样式和动画
- **JavaScript**: 交互逻辑
- **Font Awesome**: 图标库

## 安装和运行

### 1. 克隆项目

```bash
git clone <repository-url>
cd arxiv_summarizer
```

### 2. 使用conda创建虚拟环境

```bash
# 创建conda虚拟环境
conda create -n arxiv_summarizer python=3.11

# 激活虚拟环境
conda activate arxiv_summarizer

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

在backend目录下创建`.env`文件：

```env
# 模型配置
MODEL_TYPE=openai  # 可选: openai 或 ollama

# OpenAI API配置 (当MODEL_TYPE=openai时使用)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Ollama配置 (当MODEL_TYPE=ollama时使用)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:8b

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=True

# 其他配置
MAX_CONTENT_LENGTH=16777216  # 16MB
```

**配置说明**:
- 使用OpenAI: 设置`MODEL_TYPE=openai`并配置`OPENAI_API_KEY`
- 使用Ollama: 设置`MODEL_TYPE=ollama`并确保Ollama服务运行
- 详细配置说明请参考`backend/env_setup.md`

### 4. 启动后端服务

```bash
# 在backend目录下
python app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 5. 启动前端

在frontend目录下，使用任意HTTP服务器启动前端：

```bash
# 使用Python内置服务器
python -m http.server 8000

# 或使用Node.js的http-server
npx http-server -p 8000

# 或直接双击index.html文件
```

前端将在 `http://localhost:8000` 启动。

## 使用方法

1. **选择模型**: 在模型设置区域选择使用OpenAI API或Ollama本地模型
2. **测试模型**: 点击"测试模型"按钮验证模型连接状态
3. **搜索论文**: 在搜索框中输入关键词（如"machine learning"、"deep learning"等）
4. **查看结果**: 浏览搜索结果，查看论文标题、作者、摘要等信息
5. **生成总结**: 点击任意论文卡片，系统将自动下载PDF并生成AI总结
6. **阅读总结**: 查看结构化的论文总结，包括背景、方法、结果等

## API接口

### 搜索论文
```
POST /api/search
Content-Type: application/json

{
    "query": "machine learning",
    "max_results": 10
}
```

### 生成总结
```
POST /api/summarize
Content-Type: application/json

{
    "paper_id": "arxiv_id",
    "pdf_url": "pdf_url",
    "abstract": "paper_abstract"
}
```

### 健康检查
```
GET /api/health
```

### 获取模型信息
```
GET /api/models
```

### 切换模型
```
POST /api/model/switch
Content-Type: application/json

{
    "model_type": "openai",
    "model_name": "gpt-4"
}
```

### 测试模型
```
POST /api/model/test
```

## 配置说明

### 环境变量

- `MODEL_TYPE`: 模型类型（openai/ollama）
- `OPENAI_API_KEY`: OpenAI API密钥（使用OpenAI时必需）
- `OPENAI_MODEL`: OpenAI模型名称
- `OLLAMA_BASE_URL`: Ollama服务地址
- `OLLAMA_MODEL`: Ollama模型名称
- `FLASK_ENV`: Flask环境（development/production）
- `FLASK_DEBUG`: 调试模式开关
- `MAX_CONTENT_LENGTH`: 最大文件上传大小

### 模型配置

支持两种模型类型：

**OpenAI模型**:
- GPT-3.5-turbo（推荐，性价比高）
- GPT-4（更高质量）
- GPT-4-turbo-preview（最新版本）

**Ollama本地模型**:
- llama2（7B参数，推荐）
- llama2:13b（13B参数，更高质量）
- mistral（7B参数，快速）
- codellama（代码专用）

## 故障排除

### 常见问题

1. **后端启动失败**
   - 检查Python虚拟环境是否激活
   - 确认所有依赖已安装
   - 检查环境变量配置是否正确

2. **前端无法连接后端**
   - 确认后端服务正在运行
   - 检查端口5000是否被占用
   - 查看浏览器控制台错误信息

3. **模型连接失败**
   - **OpenAI**: 检查API密钥是否有效，确认API配额是否充足
   - **Ollama**: 确认Ollama服务正在运行，检查模型是否已下载
   - 使用"测试模型"功能诊断连接问题

4. **PDF解析失败**
   - 某些PDF可能无法解析，系统会自动使用摘要
   - 检查网络连接是否正常

5. **模型切换失败**
   - 确认目标模型已正确安装（Ollama）或API密钥有效（OpenAI）
   - 检查模型名称是否正确
   - 查看后端日志获取详细错误信息

### 日志查看

后端日志会显示在控制台中，包括：
- 搜索请求和结果
- PDF下载和解析状态
- API调用错误信息

## 开发说明

### 添加新功能

1. **后端**: 在`app.py`中添加新的路由和功能
2. **前端**: 在`script.js`中添加对应的API调用和UI更新
3. **样式**: 在`style.css`中添加新的样式规则

### 自定义总结模板

修改`app.py`中的`system_message`来调整总结格式：

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 联系方式

如有问题或建议，请通过GitHub Issues或邮箱1398954987@qq.com联系。
