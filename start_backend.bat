@echo off
chcp 65001 >nul
echo 启动arXiv论文搜索与总结工具后端服务...

echo 启动Ollama服务...
set OLLAMA_MODELS=E:\Ollama_models
start /b ollama serve

echo 等待Ollama服务启动...
timeout /t 5 /nobreak >nul

cd backend
start cmd /k "call conda activate arxivsum-dev && python app.py"
pause
