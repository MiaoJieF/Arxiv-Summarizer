# Ollama本地模型设置指南

## 什么是Ollama？

Ollama是一个开源工具，可以在本地运行大型语言模型，无需依赖外部API服务。它支持多种开源模型，包括Llama 2、Mistral、Code Llama等。

## 安装Ollama

### Windows

1. 访问 [Ollama官网](https://ollama.ai/)
2. 下载Windows安装包
3. 运行安装程序
4. 安装完成后，Ollama会自动添加到系统PATH

### macOS

```bash
# 使用Homebrew安装
brew install ollama

# 或下载安装包
# 访问 https://ollama.ai/ 下载macOS安装包
```

### Linux

```bash
# 使用curl安装
curl -fsSL https://ollama.ai/install.sh | sh
```

## 启动Ollama服务

```bash
# 启动Ollama服务
ollama serve
```

服务启动后会在 `http://localhost:11434` 运行。

## 下载模型

### 推荐模型

#### 1. Llama 2 (推荐)
```bash
# 7B参数版本（推荐，平衡性能和资源使用）
ollama pull llama2

# 13B参数版本（更高质量，需要更多内存）
ollama pull llama2:13b

# 70B参数版本（最高质量，需要大量内存）
ollama pull llama2:70b
```

#### 2. Mistral (快速)
```bash
# 7B参数，速度快
ollama pull mistral
```

#### 3. Code Llama (代码专用)
```bash
# 代码生成和解释
ollama pull codellama
```

#### 4. 其他模型
```bash
# 对话优化模型
ollama pull neural-chat

# 指令跟随模型
ollama pull starling-lm

# 对话模型
ollama pull vicuna

# 无审查版本
ollama pull wizard-vicuna-uncensored
```

## 验证安装

```bash
# 测试模型是否正常工作
ollama run llama2

# 在交互式界面中输入测试问题
# 输入 "Hello, how are you?" 测试响应
# 输入 /bye 退出
```

## 配置项目使用Ollama

1. 在`backend`目录下创建`.env`文件：

```env
# 模型配置
MODEL_TYPE=ollama

# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=True
```

2. 启动后端服务：

```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac
python app.py
```

3. 启动前端服务：

```bash
cd frontend
python -m http.server 8000
```

4. 在Web界面中：
   - 选择"Ollama 本地模型"
   - 选择已下载的模型
   - 点击"测试模型"验证连接
   - 开始使用！

## 性能建议

### 硬件要求

| 模型 | 最小内存 | 推荐内存 | 说明 |
|------|----------|----------|------|
| llama2 (7B) | 8GB | 16GB | 平衡性能和资源 |
| llama2:13b | 16GB | 32GB | 更高质量 |
| llama2:70b | 64GB | 128GB | 最高质量 |
| mistral (7B) | 8GB | 16GB | 速度快 |
| codellama | 8GB | 16GB | 代码专用 |

### 优化建议

1. **内存不足时**：
   - 使用较小的模型（如llama2 7B）
   - 关闭其他占用内存的应用程序

2. **速度优化**：
   - 使用SSD存储
   - 确保有足够的可用内存
   - 考虑使用GPU加速（如果支持）

3. **质量优化**：
   - 使用更大的模型（如llama2:13b）
   - 调整temperature参数

## 常见问题

### 1. 模型下载失败
```bash
# 检查网络连接
ping ollama.ai

# 重新下载
ollama pull llama2
```

### 2. 内存不足
- 关闭其他应用程序
- 使用较小的模型
- 检查系统内存使用情况

### 3. 服务启动失败
```bash
# 检查端口是否被占用
netstat -an | grep 11434

# 重启Ollama服务
ollama serve
```

### 4. 模型响应慢
- 确保有足够的可用内存
- 使用SSD存储
- 考虑使用更快的模型（如mistral）

## 高级配置

### 自定义模型配置

创建自定义模型文件 `Modelfile`：

```dockerfile
FROM llama2

# 设置系统提示
SYSTEM "你是一个专业的学术论文总结助手。"

# 设置参数
PARAMETER temperature 0.7
PARAMETER top_p 0.9
```

```bash
# 创建自定义模型
ollama create my-custom-model -f Modelfile

# 使用自定义模型
ollama run my-custom-model
```

### 环境变量配置

```bash
# 设置Ollama主机
export OLLAMA_HOST=0.0.0.0:11434

# 设置模型存储路径
export OLLAMA_MODELS=/path/to/models
```

## 更多资源

- [Ollama官方文档](https://ollama.ai/docs)
- [模型库](https://ollama.ai/library)
- [GitHub仓库](https://github.com/jmorganca/ollama)
- [社区论坛](https://github.com/jmorganca/ollama/discussions)
