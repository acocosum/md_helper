import openai
import numpy as np
from typing import List
import streamlit as st

# 初始化变量
openai_client = None
api_base = None

def initialize_openai(api_key: str, custom_api_base: str = None) -> None:
    """
    初始化OpenAI客户端
    
    Args:
        api_key (str): OpenAI API密钥
        custom_api_base (str, optional): 自定义API接口地址，如果为None则使用官方API
    """
    global openai_client, api_base
    # 重要：不再设置全局的 openai.api_key，避免请求被转发到官方API
    # openai.api_key = api_key  # 删除此行
    api_base = custom_api_base
    
    if custom_api_base:
        # 对于自定义API地址，我们需要确保它不包含具体的端点
        base_url = custom_api_base
        if "/chat/completions" in base_url:
            # 如果URL包含具体的chat/completions端点，则提取基础URL
            base_url = base_url.replace("/chat/completions", "")
        if "/embeddings" in base_url:
            # 如果URL包含embeddings端点，也要移除
            base_url = base_url.replace("/embeddings", "")
            
        print(f"使用自定义API地址: {base_url}")
        openai_client = openai.OpenAI(api_key=api_key, base_url=base_url)
    else:
        openai_client = openai.OpenAI(api_key=api_key)
    
    st.session_state.openai_client = openai_client

def get_embedding(text: str) -> List[float]:
    """
    使用OpenAI API获取文本的embedding向量
    
    Args:
        text (str): 需要转换为向量的文本
        
    Returns:
        List[float]: 文本的embedding向量
        
    Raises:
        ValueError: 如果API未初始化或调用失败
    """
    if not openai_client:
        raise ValueError("OpenAI API尚未初始化，请先设置API Key")
    
    # 确保文本不为空
    if not text or text.isspace():
        text = "empty"
    
    try:
        # 调用OpenAI API获取文本向量
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        
        # 提取向量
        embedding = response.data[0].embedding
        return embedding
    
    except Exception as e:
        print(f"获取embedding时出错: {str(e)}")
        # 在出错时返回零向量，避免程序崩溃
        # 在实际应用中，您可能希望以更好的方式处理这种错误
        return [0.0] * 1536  # text-embedding-ada-002 模型的维度是1536