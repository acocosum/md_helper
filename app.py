import streamlit as st
import os
from modules.markdown_loader import load_markdown
from modules.text_splitter import split_text
from modules.embedder import get_embedding, initialize_openai
from modules.retriever import retrieve
from modules.qa_chain_new import generate_answer

# 页面配置
st.set_page_config(
    page_title="个人知识库助手",
    page_icon="📚",
    layout="wide"
)

# 初始化会话状态
if 'chunks' not in st.session_state:
    st.session_state.chunks = []
if 'embeddings' not in st.session_state:
    st.session_state.embeddings = []
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False
if 'openai_key' not in st.session_state:
    st.session_state.openai_key = ""
if 'api_base' not in st.session_state:
    st.session_state.api_base = ""

# 标题
st.title("📚 个人知识库助手")
st.markdown("上传Markdown文件，通过AI快速获取知识库内容的答案")

# 侧边栏 - OpenAI API设置
with st.sidebar:
    st.header("配置")
    # 获取API key和自定义API地址
    api_key = st.text_input("输入OpenAI API Key", type="password", value=st.session_state.openai_key)
    custom_api_base = st.text_input("自定义API地址(可选)", value=st.session_state.api_base or "https://40.chatgptsb.net/v1")

    # 如果用户提供了自定义API地址，确保它只包含基础URL部分
    if custom_api_base and "/chat/completions" in custom_api_base:
        custom_api_base = custom_api_base.replace("/chat/completions", "")

    if api_key:
        st.session_state.openai_key = api_key
        st.session_state.api_base = custom_api_base
        if custom_api_base:
            initialize_openai(api_key, custom_api_base)
            st.success(f"API已配置：使用自定义API地址 {custom_api_base}")
        else:
            initialize_openai(api_key)
            st.success("API已配置：使用OpenAI官方API")
    
    st.markdown("---")
    st.markdown("### 参数设置")
    chunk_size = st.slider("文本块大小", min_value=100, max_value=1000, value=500, step=100,
                         help="每个文本块的字符数量")
    chunk_overlap = st.slider("文本块重叠", min_value=0, max_value=200, value=50, step=10,
                            help="相邻文本块的重叠字符数")
    top_k = st.slider("检索数量", min_value=1, max_value=10, value=3, step=1,
                    help="每次问答检索的相关文本块数量")
    
    st.markdown("---")
    st.markdown("### 关于")
    st.info("这是一个基于OpenAI API的个人知识库助手，将您的Markdown笔记转化为可查询的知识库。")

# 文件上传区域
uploaded_file = st.file_uploader("上传Markdown文件", type=["md"], 
                              help="选择一个Markdown格式的文件")

# 处理上传的文件
if uploaded_file and not st.session_state.file_processed:
    with st.spinner("处理文件中..."):
        # 读取并解析Markdown文件
        content = load_markdown(uploaded_file)
        
        # 文本切分
        chunks = split_text(content, chunk_size=chunk_size, overlap=chunk_overlap)
        st.session_state.chunks = chunks
        
        if st.session_state.openai_key:
            # 计算Embedding
            with st.status("生成文本向量中，请稍候..."):
                embeddings = [get_embedding(chunk) for chunk in chunks]
                st.session_state.embeddings = embeddings
                st.session_state.file_processed = True
                st.success(f"文件处理完成，共切分为{len(chunks)}个文本块")
        else:
            st.warning("请先设置OpenAI API Key")

# 如果文件已处理，显示问答界面
if st.session_state.file_processed:
    st.markdown("---")
    st.subheader("💬 向您的知识库提问")
    
    # 问题输入区域
    question = st.text_input("输入您的问题", placeholder="例如：这个项目的主要功能是什么？")
    
    if question:
        if len(st.session_state.chunks) > 0 and len(st.session_state.embeddings) > 0:
            with st.spinner("思考中..."):
                # 问题向量化
                question_embedding = get_embedding(question)
                
                # 检索相关文本块
                relevant_indices = retrieve(question_embedding, st.session_state.embeddings, top_k=top_k)
                relevant_chunks = [st.session_state.chunks[i] for i in relevant_indices]
                
                # 生成答案
                answer = generate_answer(question, relevant_chunks)
                
                # 显示答案
                st.markdown("### 回答")
                st.markdown(answer)
                
                # 显示相关内容（可折叠）
                with st.expander("查看相关文本块"):
                    for i, chunk in enumerate(relevant_chunks):
                        st.markdown(f"**文本块 {i+1}**")
                        st.info(chunk)
        else:
            st.error("知识库中没有内容，请上传并处理Markdown文件")
