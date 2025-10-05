#!/usr/bin/env python3
"""
模型测试脚本
用于测试OpenAI和Ollama模型的连接和响应
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

API_BASE_URL = 'http://localhost:5000/api'

def test_health():
    """测试API健康状态"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API服务正常运行")
            return True
        else:
            print(f"❌ API服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到API服务: {e}")
        return False

def test_models():
    """测试模型信息获取"""
    try:
        response = requests.get(f"{API_BASE_URL}/models")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 当前模型类型: {data['current_model_type']}")
            print(f"✅ 当前模型: {data['current_model']}")
            print("✅ 可用模型列表:")
            for model_type, models in data['available_models'].items():
                print(f"   {model_type}: {', '.join(models)}")
            return True
        else:
            print(f"❌ 获取模型信息失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取模型信息异常: {e}")
        return False

def test_model_switch(model_type, model_name):
    """测试模型切换"""
    try:
        response = requests.post(f"{API_BASE_URL}/model/switch", 
                               json={
                                   'model_type': model_type,
                                   'model_name': model_name
                               })
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 模型切换成功: {data['model_name']}")
            return True
        else:
            data = response.json()
            print(f"❌ 模型切换失败: {data.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 模型切换异常: {e}")
        return False

def test_model_response():
    """测试模型响应"""
    try:
        response = requests.post(f"{API_BASE_URL}/model/test")
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print(f"✅ 模型测试成功: {data['response']}")
                return True
            else:
                print(f"❌ 模型测试失败: {data.get('error', '未知错误')}")
                return False
        else:
            data = response.json()
            print(f"❌ 模型测试失败: {data.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 模型测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始测试arXiv论文搜索与总结工具...")
    print("=" * 50)
    
    # 测试API健康状态
    if not test_health():
        print("\n❌ API服务未运行，请先启动后端服务")
        print("运行命令: cd backend && python app.py")
        return
    
    print()
    
    # 测试模型信息
    if not test_models():
        print("\n❌ 无法获取模型信息")
        return
    
    print()
    
    # 测试当前模型响应
    print("🔍 测试当前模型响应...")
    if not test_model_response():
        print("❌ 当前模型响应测试失败")
        return
    
    print()
    
    # 测试模型切换（如果配置了OpenAI）
    if os.getenv('OPENAI_API_KEY'):
        print("🔄 测试OpenAI模型切换...")
        test_model_switch('openai', 'gpt-3.5-turbo')
        test_model_response()
        print()
    
    # 测试Ollama模型切换（如果Ollama服务运行）
    print("🔄 测试Ollama模型切换...")
    if test_model_switch('ollama', 'llama2'):
        test_model_response()
    
    print()
    print("=" * 50)
    print("✅ 测试完成！")
    print("\n💡 提示:")
    print("- 如果OpenAI测试失败，请检查API密钥配置")
    print("- 如果Ollama测试失败，请确保Ollama服务正在运行")
    print("- 详细配置说明请参考 backend/env_setup.md")

if __name__ == "__main__":
    main()
