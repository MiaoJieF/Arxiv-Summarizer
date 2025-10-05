@echo off
echo 启动arXiv论文搜索与总结工具前端服务...
cd frontend
python -m http.server 8000
pause
