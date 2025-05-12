from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from typing import List, Dict, Any, Optional
import streamlit as st
import tempfile
import os

def load_markdown_with_langchain(file) -> List[Any]:
    """
    使用LangChain加载Markdown文件
    
    Args:
        file: 上传的文件对象
        
    Returns:
        List: 文档对象列表
    """
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as temp_file:
        temp_file.write(file.getvalue())
        temp_path = temp_file.name
    
    try:
        # 使用LangChain加载临时文件
        loader = UnstructuredMarkdownLoader(temp_path)
        documents = loader.load()
        return documents
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)

def split_documents(documents: List[Any], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Any]:
    """
    使用LangChain切分文档
    
    Args:
        documents: 文档对象列表
        chunk_size: 文本块大小
        chunk_overlap: 文本块重叠度
        
    Returns:
        List: 切分后的文档块列表
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = splitter.split_documents(documents)
    return chunks

def get_openai_embeddings(api_key: str, api_base: Optional[str] = None) -> OpenAIEmbeddings:
    """
    创建OpenAI嵌入模型实例
    
    Args:
        api_key: OpenAI API密钥
        api_base: 可选的自定义API基础URL
        
    Returns:
        OpenAIEmbeddings: 嵌入模型实例
    """
    if api_base:
        # 处理API URL
        base_url = api_base
        if "/chat/completions" in base_url:
            base_url = base_url.replace("/chat/completions", "")
        if "/embeddings" in base_url:
            base_url = base_url.replace("/embeddings", "")
            
        # 使用自定义API
        return OpenAIEmbeddings(
            openai_api_key=api_key,
            openai_api_base=base_url,
            model="text-embedding-ada-002"
        )
    else:
        # 使用官方API
        return OpenAIEmbeddings(
            openai_api_key=api_key,
            model="text-embedding-ada-002"
        )

def create_faiss_index(documents: List[Any], embeddings) -> FAISS:
    """
    为文档创建FAISS向量索引
    
    Args:
        documents: 文档块列表
        embeddings: 嵌入模型实例
        
    Returns:
        FAISS: FAISS向量存储对象
    """
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

def get_chat_model(api_key: str, api_base: Optional[str] = None) -> ChatOpenAI:
    """
    创建ChatOpenAI模型实例
    
    Args:
        api_key: OpenAI API密钥
        api_base: 可选的自定义API基础URL
        
    Returns:
        ChatOpenAI: 聊天模型实例
    """
    if api_base:
        # 处理API URL
        base_url = api_base
        if "/chat/completions" in base_url:
            base_url = base_url.replace("/chat/completions", "")
        if "/embeddings" in base_url:
            base_url = base_url.replace("/embeddings", "")
            
        # 使用自定义API
        return ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base=base_url,
            temperature=0.3,
            model="gpt-3.5-turbo"
        )
    else:
        # 使用官方API
        return ChatOpenAI(
            openai_api_key=api_key,
            temperature=0.3,
            model="gpt-3.5-turbo"
        )

def create_qa_chain(llm, vectorstore: FAISS) -> RetrievalQA:
    """
    创建问答检索链
    
    Args:
        llm: 语言模型实例
        vectorstore: 向量存储对象
        
    Returns:
        RetrievalQA: 问答检索链
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    return qa_chain

def query_knowledge_base(query: str, qa_chain) -> Dict[str, Any]:
    """
    查询知识库并获取回答
    
    Args:
        query: 用户问题
        qa_chain: 问答检索链
        
    Returns:
        Dict: 包含回答和来源文档的字典
    """
    result = qa_chain({"query": query})
    
    # 提取回答和来源文档
    answer = result.get("result", "")
    source_documents = result.get("source_documents", [])
    
    return {
        "answer": answer,
        "source_documents": source_documents
    }
