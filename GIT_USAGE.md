# Git使用说明

## 项目Git配置

本项目已经配置了合适的`.gitignore`文件，会自动忽略以下文件：

### 被忽略的文件类型

1. **Python相关**：
   - `__pycache__/` - Python缓存文件
   - `*.pyc`, `*.pyo` - 编译的Python文件
   - `venv/` - 虚拟环境目录
   - `*.egg-info/` - 包信息目录

2. **环境变量和敏感信息**：
   - `.env` - 环境变量文件（包含API密钥）
   - `backend/.env` - 后端环境变量
   - `config.ini` - 配置文件
   - `secrets.json` - 密钥文件

3. **系统文件**：
   - `.DS_Store` - macOS系统文件
   - `Thumbs.db` - Windows缩略图缓存
   - `*.tmp`, `*.temp` - 临时文件

4. **IDE和编辑器**：
   - `.vscode/` - VS Code配置
   - `.idea/` - PyCharm配置
   - `*.sublime-project` - Sublime Text项目文件

5. **模型文件**：
   - `models/` - 本地模型文件目录
   - `*.bin`, `*.safetensors`, `*.gguf` - 模型文件
   - `*.pth`, `*.pt`, `*.ckpt` - PyTorch模型文件

6. **其他**：
   - `logs/` - 日志文件
   - `*.log` - 日志文件
   - `cache/` - 缓存目录
   - `tmp/`, `temp/` - 临时目录

## 常用Git命令

### 查看状态
```bash
# 查看当前状态
git status

# 查看被忽略的文件
git status --ignored

# 查看文件差异
git diff
```

### 添加和提交
```bash
# 添加所有文件
git add .

# 添加特定文件
git add filename

# 提交更改
git commit -m "提交说明"

# 查看提交历史
git log --oneline
```

### 分支管理
```bash
# 创建新分支
git checkout -b feature-branch

# 切换分支
git checkout main

# 合并分支
git merge feature-branch

# 删除分支
git branch -d feature-branch
```

### 远程仓库
```bash
# 添加远程仓库
git remote add origin <repository-url>

# 推送到远程
git push -u origin main

# 拉取更新
git pull origin main

# 克隆仓库
git clone <repository-url>
```

## 项目特定注意事项

### 1. 环境变量文件
- **永远不要**提交`.env`文件
- 使用`backend/env_setup.md`作为配置模板
- 在部署时手动创建`.env`文件

### 2. 虚拟环境
- `backend/venv/`目录已被忽略
- 每个开发者需要自己创建虚拟环境
- 使用`requirements.txt`安装依赖

### 3. 模型文件
- 大型模型文件不应提交到Git
- 使用Ollama下载模型到本地
- 在README中说明如何获取模型

### 4. 敏感信息
- API密钥、数据库密码等敏感信息不要提交
- 使用环境变量或配置文件管理
- 在文档中说明如何配置

## 开发工作流

### 1. 开始新功能
```bash
# 创建功能分支
git checkout -b feature/new-feature

# 进行开发...
# 添加文件
git add .

# 提交更改
git commit -m "Add new feature: description"
```

### 2. 合并到主分支
```bash
# 切换回主分支
git checkout main

# 拉取最新更改
git pull origin main

# 合并功能分支
git merge feature/new-feature

# 推送更改
git push origin main
```

### 3. 处理冲突
```bash
# 拉取时如果有冲突
git pull origin main

# 解决冲突后
git add .
git commit -m "Resolve merge conflicts"
```

## 最佳实践

1. **提交信息**：
   - 使用清晰、描述性的提交信息
   - 使用英文或中文，保持一致性
   - 格式：`类型: 简短描述`

2. **分支命名**：
   - `feature/功能名称`
   - `bugfix/问题描述`
   - `hotfix/紧急修复`

3. **提交频率**：
   - 经常提交，每次提交包含一个完整的功能
   - 避免大量文件的一次性提交
   - 提交前检查文件状态

4. **代码审查**：
   - 重要更改前进行代码审查
   - 使用Pull Request进行协作
   - 保持代码质量

## 故障排除

### 1. 误提交敏感文件
```bash
# 从Git历史中移除文件
git rm --cached .env
git commit -m "Remove .env from tracking"

# 确保.gitignore包含该文件
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to .gitignore"
```

### 2. 撤销更改
```bash
# 撤销工作区更改
git checkout -- filename

# 撤销暂存区更改
git reset HEAD filename

# 撤销最后一次提交
git reset --soft HEAD~1
```

### 3. 查看文件历史
```bash
# 查看文件修改历史
git log --follow filename

# 查看文件具体更改
git show commit-hash:filename
```

## 部署注意事项

1. **生产环境**：
   - 确保`.env`文件正确配置
   - 检查所有依赖是否安装
   - 验证模型连接状态

2. **CI/CD**：
   - 使用环境变量而不是配置文件
   - 自动化测试和部署
   - 监控部署状态

3. **备份**：
   - 定期备份重要数据
   - 使用版本控制管理配置
   - 文档化部署流程
