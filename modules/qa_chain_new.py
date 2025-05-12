import openai
from typing import List
import streamlit as st
from modules.embedder import api_base

def generate_answer(question: str, context_chunks: List[str]) -> str:
    """
    基于上下文生成问题的答案
    
    Args:
        question (str): 用户的问题
        context_chunks (List[str]): 相关的文本块列表
        
    Returns:
        str: 生成的答案
    """
    # 检查OpenAI客户端是否可用
    openai_client = st.session_state.get("openai_client", None)
    if not openai_client:
        return "错误: OpenAI API 客户端未初始化，请先设置API Key"
    
    # 合并上下文
    context = "\n\n".join(context_chunks)
    
    # 构造prompt
    prompt = f"""
你是一个基于知识库的智能助手。请基于我提供的上下文信息，回答用户的问题。
如果上下文中没有足够的信息回答问题，请直接说明"基于提供的信息，我无法回答这个问题"，不要编造答案。

上下文信息:
{context}

用户问题: {question}

请提供详细、准确的回答，并尽可能使用上下文中的原文表述。回答应该保持专业、友好的语气，并直接针对问题给出信息。
"""

    try:
        # 使用st.session_state中的 openai_client
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # 可以根据需求更换模型
            messages=[
                {"role": "system", "content": "你是一个智能知识库助手，根据提供的上下文回答用户问题。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # 降低温度以获得更确定的回答
            max_tokens=800  # 限制回答长度
        )
        
        # 提取生成的回答文本
        answer = response.choices[0].message.content
        return answer
        
    except Exception as e:
        # 发生错误时返回错误信息
        error_msg = str(e)
        print(f"生成回答时出错: {error_msg}")
        return f"生成回答时出错: {error_msg}"