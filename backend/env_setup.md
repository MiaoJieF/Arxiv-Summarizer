# 环境变量配置说明

## 创建.env文件

在backend目录下创建`.env`文件，并添加以下配置：

```env
# 模型配置
MODEL_TYPE=openai  # 可选: openai 或 ollama

# OpenAI API配置 (当MODEL_TYPE=openai时使用)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Ollama配置 (当MODEL_TYPE=ollama时使用)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=True

# 其他配置
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## 配置说明

### 使用OpenAI API

1. 设置 `MODEL_TYPE=openai`
2. 获取OpenAI API密钥：
   - 访问 [OpenAI官网](https://platform.openai.com/)
   - 注册或登录账户
   - 进入API Keys页面
   - 创建新的API密钥
   - 将密钥复制到`OPENAI_API_KEY`字段
3. 选择模型：`gpt-3.5-turbo`、`gpt-4`、`gpt-4-turbo-preview`

### 使用Ollama本地模型

1. 设置 `MODEL_TYPE=ollama`
2. 安装并启动Ollama：
   ```bash
   # 安装Ollama (访问 https://ollama.ai/)
   # 启动Ollama服务
   ollama serve
   ```
3. 下载模型：
   ```bash
   # 下载Llama 2模型
   ollama pull llama2
   
   # 或下载其他模型
   ollama pull mistral
   ollama pull codellama
   ```
4. 配置模型名称：`llama2`、`mistral`、`codellama`等

## 支持的模型

### OpenAI模型
- `gpt-3.5-turbo` (推荐，性价比高)
- `gpt-4` (更高质量)
- `gpt-4-turbo-preview` (最新版本)

### Ollama模型
- `llama2` (7B参数，推荐)
- `llama2:13b` (13B参数，更高质量)
- `llama2:70b` (70B参数，最高质量，需要更多内存)
- `mistral` (7B参数，快速)
- `codellama` (代码专用)
- `neural-chat` (对话优化)
- `starling-lm` (指令跟随)
- `vicuna` (对话模型)
- `wizard-vicuna-uncensored` (无审查版本)

## 注意事项

- 请勿将`.env`文件提交到版本控制系统
- 确保API密钥的安全性
- 使用Ollama时，确保服务正在运行
- 不同模型的内存需求不同，请根据硬件选择合适的模型
- 可以在运行时通过Web界面切换模型，无需重启服务
