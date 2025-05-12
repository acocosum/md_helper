import streamlit as st
import os
from modules.langchain_helper import (
    load_markdown_with_langchain, 
    split_documents, 
    get_openai_embeddings, 
    create_faiss_index,
    get_chat_model,
    create_qa_chain,
    query_knowledge_base
)

# 页面配置
st.set_page_config(
    page_title="个人知识库助手 (LangChain + FAISS)",
    page_icon="📚",
    layout="wide"
)

# 初始化会话状态
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False
if 'openai_key' not in st.session_state:
    st.session_state.openai_key = ""
if 'api_base' not in st.session_state:
    st.session_state.api_base = ""
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None

# 标题
st.title("📚 个人知识库助手 (LangChain + FAISS)")
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
    if custom_api_base and "/embeddings" in custom_api_base:
        custom_api_base = custom_api_base.replace("/embeddings", "")

    if api_key:
        st.session_state.openai_key = api_key
        st.session_state.api_base = custom_api_base
        if custom_api_base:
            st.success(f"API已配置：使用自定义API地址 {custom_api_base}")
        else:
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
    st.info("这是一个基于LangChain框架和FAISS向量数据库的个人知识库助手，将您的Markdown笔记转化为可查询的知识库。")

# 文件上传区域
uploaded_file = st.file_uploader("上传Markdown文件", type=["md"], 
                              help="选择一个Markdown格式的文件")

# 处理上传的文件
if uploaded_file and not st.session_state.file_processed:
    if st.session_state.openai_key:
        with st.spinner("处理文件中..."):
            try:
                # 使用LangChain加载和处理Markdown文件
                with st.status("加载Markdown文件..."):
                    documents = load_markdown_with_langchain(uploaded_file)
                
                # 文本切分
                with st.status("切分文档..."):
                    chunks = split_documents(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    st.session_state.doc_chunks = chunks
                
                # 创建嵌入模型
                with st.status("初始化嵌入模型..."):
                    embeddings = get_openai_embeddings(
                        api_key=st.session_state.openai_key, 
                        api_base=st.session_state.api_base
                    )
                
                # 创建FAISS索引
                with st.status("创建向量索引 (FAISS)..."):
                    vectorstore = create_faiss_index(chunks, embeddings)
                    st.session_state.vectorstore = vectorstore
                
                # 创建语言模型
                with st.status("初始化语言模型..."):
                    llm = get_chat_model(
                        api_key=st.session_state.openai_key, 
                        api_base=st.session_state.api_base
                    )
                
                # 创建问答链
                with st.status("构建问答链..."):
                    qa_chain = create_qa_chain(llm, vectorstore)
                    st.session_state.qa_chain = qa_chain
                
                # 更新状态
                st.session_state.file_processed = True
                st.success(f"文件处理完成，共切分为{len(chunks)}个文本块")
                
            except Exception as e:
                st.error(f"处理文件时出错: {str(e)}")
    else:
        st.warning("请先设置OpenAI API Key")

# 如果文件已处理，显示问答界面
if st.session_state.file_processed and st.session_state.qa_chain:
    st.markdown("---")
    st.subheader("💬 向您的知识库提问")
    
    # 问题输入区域
    question = st.text_input("输入您的问题", placeholder="例如：这个项目的主要功能是什么？")
    
    if question:
        with st.spinner("思考中..."):
            try:
                # 查询知识库
                result = query_knowledge_base(question, st.session_state.qa_chain)
                
                # 获取答案和来源文档
                answer = result["answer"]
                source_docs = result["source_documents"]
                
                # 显示答案
                st.markdown("### 回答")
                st.markdown(answer)
                
                # 显示相关内容（可折叠）
                with st.expander("查看相关文本块"):
                    for i, doc in enumerate(source_docs):
                        st.markdown(f"**文本块 {i+1}**")
                        st.info(doc.page_content)
                        st.caption(f"相关度：{i+1}/{len(source_docs)}")
                        
            except Exception as e:
                st.error(f"生成回答时出错: {str(e)}")
