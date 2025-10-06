// API基础URL
const API_BASE_URL = 'http://localhost:5000/api';

// DOM元素
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const maxResults = document.getElementById('maxResults');
const sortBy = document.getElementById('sortBy');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const results = document.getElementById('results');
const papersList = document.getElementById('papersList');
const summary = document.getElementById('summary');
const summaryContent = document.getElementById('summaryContent');
const summaryLoading = document.getElementById('summaryLoading');

// 模型相关元素
const modelType = document.getElementById('modelType');
const modelName = document.getElementById('modelName');
const testModelBtn = document.getElementById('testModelBtn');
const switchModelBtn = document.getElementById('switchModelBtn');
const currentModel = document.getElementById('currentModel');
const modelStatusIcon = document.getElementById('modelStatusIcon');

// 事件监听器
searchBtn.addEventListener('click', handleSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});

// 模型相关事件监听器
modelType.addEventListener('change', updateModelOptions);
testModelBtn.addEventListener('click', testCurrentModel);
switchModelBtn.addEventListener('click', switchModel);

// 搜索论文
async function handleSearch() {
    const query = searchInput.value.trim();
    if (!query) {
        showError('请输入搜索关键词');
        return;
    }

    hideError();
    showLoading();
    hideResults();
    hideSummary();

    try {
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                max_results: parseInt(maxResults.value),
                sort_by: sortBy.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || '搜索失败');
        }

        displayPapers(data.papers);
        hideLoading();
        showResults();

    } catch (err) {
        hideLoading();
        showError(`搜索失败: ${err.message}`);
    }
}

// 显示论文列表
function displayPapers(papers) {
    papersList.innerHTML = '';

    if (papers.length === 0) {
        papersList.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 40px;">未找到相关论文</p>';
        return;
    }

    papers.forEach(paper => {
        const paperCard = createPaperCard(paper);
        papersList.appendChild(paperCard);
    });
}

// 创建论文卡片
function createPaperCard(paper) {
    const card = document.createElement('div');
    card.className = 'paper-card';
    card.onclick = () => summarizePaper(paper);

    const authors = paper.authors.join(', ');
    const publishedDate = new Date(paper.published).toLocaleDateString('zh-CN');
    const categories = paper.categories.map(cat => 
        `<span class="category-tag">${cat}</span>`
    ).join('');

    card.innerHTML = `
        <div class="paper-title">${paper.title}</div>
        <div class="paper-authors">作者: ${authors}</div>
        <div class="paper-abstract">${paper.abstract}</div>
        <div class="paper-meta">
            <div class="paper-date">
                <i class="fas fa-calendar"></i>
                ${publishedDate}
            </div>
            <div class="paper-categories">${categories}</div>
        </div>
    `;

    return card;
}

// 总结论文
async function summarizePaper(paper) {
    hideError();
    showSummaryLoading();
    showSummary();

    try {
        const response = await fetch(`${API_BASE_URL}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                paper_id: paper.id,
                pdf_url: paper.pdf_url,
                abstract: paper.abstract
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || '总结生成失败');
        }

        displaySummary(data.summary, paper.title);
        hideSummaryLoading();

    } catch (err) {
        hideSummaryLoading();
        showError(`总结生成失败: ${err.message}`);
    }
}

// 显示总结
function displaySummary(summaryText, paperTitle) {
    summaryContent.innerHTML = `
        <h3 style="color: #495057; margin-bottom: 15px; font-size: 1.3rem;">
            <i class="fas fa-file-alt"></i> ${paperTitle}
        </h3>
        <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
            <pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">${summaryText}</pre>
        </div>
    `;
}

// 工具函数
function showLoading() {
    loading.classList.remove('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    error.classList.remove('hidden');
}

function hideError() {
    error.classList.add('hidden');
}

function showResults() {
    results.classList.remove('hidden');
}

function hideResults() {
    results.classList.add('hidden');
}

function showSummary() {
    summary.classList.remove('hidden');
}

function hideSummary() {
    summary.classList.add('hidden');
}

function showSummaryLoading() {
    summaryLoading.classList.remove('hidden');
}

function hideSummaryLoading() {
    summaryLoading.classList.add('hidden');
}

// 模型相关函数
async function updateModelOptions() {
    const selectedType = modelType.value;
    const modelOptions = {
        'openai': [
            { value: 'gpt-3.5-turbo', text: 'GPT-3.5 Turbo' },
            { value: 'gpt-4', text: 'GPT-4' },
            { value: 'gpt-4-turbo-preview', text: 'GPT-4 Turbo' }
        ],
        'ollama': [
            { value: 'llama2', text: 'Llama 2' },
            { value: 'llama2:13b', text: 'Llama 2 13B' },
            { value: 'llama2:70b', text: 'Llama 2 70B' },
            { value: 'codellama', text: 'Code Llama' },
            { value: 'mistral', text: 'Mistral' },
            { value: 'neural-chat', text: 'Neural Chat' },
            { value: 'starling-lm', text: 'Starling LM' },
            { value: 'vicuna', text: 'Vicuna' },
            { value: 'wizard-vicuna-uncensored', text: 'Wizard Vicuna' }
        ]
    };
    
    // 清空并重新填充模型选择器
    modelName.innerHTML = '';
    modelOptions[selectedType].forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option.value;
        optionElement.textContent = option.text;
        modelName.appendChild(optionElement);
    });
}

async function testCurrentModel() {
    testModelBtn.disabled = true;
    testModelBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 测试中...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/model/test`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showModelStatus('success', `模型测试成功: ${data.response}`);
        } else {
            showModelStatus('error', `模型测试失败: ${data.error}`);
        }
    } catch (err) {
        showModelStatus('error', `测试失败: ${err.message}`);
    } finally {
        testModelBtn.disabled = false;
        testModelBtn.innerHTML = '<i class="fas fa-vial"></i> 测试模型';
    }
}

async function switchModel() {
    switchModelBtn.disabled = true;
    switchModelBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 切换中...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/model/switch`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model_type: modelType.value,
                model_name: modelName.value
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showModelStatus('success', `模型切换成功: ${data.model_name}`);
            updateCurrentModelDisplay(data.model_type, data.model_name);
        } else {
            showModelStatus('error', `切换失败: ${data.error}`);
        }
    } catch (err) {
        showModelStatus('error', `切换失败: ${err.message}`);
    } finally {
        switchModelBtn.disabled = false;
        switchModelBtn.innerHTML = '<i class="fas fa-exchange-alt"></i> 切换模型';
    }
}

function showModelStatus(type, message) {
    modelStatusIcon.className = `status-icon ${type}`;
    currentModel.textContent = `当前模型: ${message}`;
    
    // 3秒后恢复正常状态
    setTimeout(() => {
        modelStatusIcon.className = 'status-icon';
    }, 3000);
}

function updateCurrentModelDisplay(modelType, modelName) {
    const displayName = modelType === 'openai' ? `OpenAI ${modelName}` : `Ollama ${modelName}`;
    currentModel.textContent = `当前模型: ${displayName}`;
}

async function loadModelInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/models`);
        const data = await response.json();
        
        // 设置当前模型类型
        modelType.value = data.current_model_type;
        
        // 更新模型选项
        await updateModelOptions();
        
        // 设置当前模型名称
        modelName.value = data.current_model;
        
        // 更新显示
        updateCurrentModelDisplay(data.current_model_type, data.current_model);
        
    } catch (err) {
        console.error('加载模型信息失败:', err.message);
    }
}

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function() {
    // 检查后端连接
    checkBackendConnection();
    // 加载模型信息
    loadModelInfo();
});

// 检查后端连接
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            throw new Error('后端服务未响应');
        }
        console.log('后端服务连接正常');
    } catch (err) {
        console.error('后端服务连接失败:', err.message);
        showError('无法连接到后端服务，请确保后端服务正在运行');
    }
}
