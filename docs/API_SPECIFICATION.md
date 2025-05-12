# 个人知识库助手 - API 接口规范

本文档详细说明个人知识库助手系统中的关键API接口、数据结构和集成规范，主要针对希望了解系统内部工作原理或进行二次开发的开发者。

## LangChain & OpenAI API 集成

本项目基于 LangChain 框架，集成 OpenAI 官方及兼容 API，支持自定义 API 地址。所有文档加载、切分、向量化、索引与问答均通过 LangChain 统一调度。

### 文档加载与切分
- 使用 `UnstructuredMarkdownLoader` 加载 Markdown 文件
- 使用 `RecursiveCharacterTextSplitter` 切分文档，支持自定义 chunk_size 和 chunk_overlap

### 向量化与索引
- 使用 `OpenAIEmbeddings` 进行文本向量化，支持自定义 API Key 和 API Base
- 使用 `FAISS` 作为向量数据库，支持高效的相似度检索

### 问答链
- 使用 `ChatOpenAI` 作为 LLM
- 通过 `RetrievalQA` 构建检索增强问答链，自动检索相关文本块并生成答案

#### 典型调用流程

```python
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# 1. 加载文档
documents = UnstructuredMarkdownLoader("your.md").load()
# 2. 切分文档
chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(documents)
# 3. 嵌入模型
embeddings = OpenAIEmbeddings(openai_api_key="sk-xxx", openai_api_base="https://xxx.com/v1")
# 4. 构建FAISS索引
vectorstore = FAISS.from_documents(chunks, embeddings)
# 5. 构建LLM
llm = ChatOpenAI(openai_api_key="sk-xxx", openai_api_base="https://xxx.com/v1")
# 6. 构建问答链
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever(), return_source_documents=True)
# 7. 查询
result = qa_chain({"query": "你的问题"})
print(result["result"])
```

## 内部模块 API

### modules/langchain_helper.py

- `load_markdown_with_langchain(file)`
  - 加载 Markdown 文件为 LangChain 文档对象
- `split_documents(documents, chunk_size, chunk_overlap)`
  - 切分文档为文本块
- `get_openai_embeddings(api_key, api_base)`
  - 获取 OpenAI 嵌入模型实例
- `create_faiss_index(documents, embeddings)`
  - 构建 FAISS 向量索引
- `get_chat_model(api_key, api_base)`
  - 获取 ChatOpenAI LLM 实例
- `create_qa_chain(llm, vectorstore)`
  - 构建检索增强问答链
- `query_knowledge_base(query, qa_chain)`
  - 查询知识库并返回答案和相关文本块

## 数据结构

- 文档块：LangChain 文档对象列表
- 向量索引：FAISS 对象
- 问答链：RetrievalQA 对象

## 自定义API集成规范

- 只需保证 API 兼容 OpenAI Embedding/Chat 格式即可
- 支持自定义 API Key 和 API Base
- 推荐使用官方或高兼容性的第三方 API

## 会话状态变量

- `st.session_state.vectorstore`：FAISS 向量索引
- `st.session_state.qa_chain`：问答链对象
- `st.session_state.file_processed`：文件处理状态
- `st.session_state.openai_key`：API Key
- `st.session_state.api_base`：API Base

## 错误处理

- 依赖 LangChain 的异常处理机制
- 常见错误如 API 401/404/429 均有友好提示

## 版本兼容性

- 推荐 LangChain >= 0.1.0
- 推荐 langchain-community >= 0.0.20
- 推荐 openai >= 1.6.0

## 结语

本项目所有 API 调用均通过 LangChain 封装，开发者可直接基于 LangChain 生态进行二次开发和扩展。
