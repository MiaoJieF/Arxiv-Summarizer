@echo off
chcp 65001 >nul
echo 启动arXiv论文搜索与总结工具后端服务...
cd backend
call venv\Scripts\activate.bat
python app.py
pause