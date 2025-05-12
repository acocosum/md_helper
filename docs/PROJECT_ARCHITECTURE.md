# 个人知识库助手 - 技术架构与实现文档（LangChain 版）

## 系统概述

本系统基于 Streamlit + LangChain + FAISS + OpenAI API/兼容API，支持 Markdown 文档上传、自动切分、向量化、索引、语义检索与 LLM 问答。

## 架构图

```
用户
  │
  ▼
Streamlit 前端（app_langchain.py）
  │
  ├─ langchain_helper.py（文档加载/切分/嵌入/索引/问答链）
  │
  └─ LangChain 生态（UnstructuredMarkdownLoader, RecursiveCharacterTextSplitter, OpenAIEmbeddings, FAISS, ChatOpenAI, RetrievalQA）
  │
  └─ OpenAI API/兼容API
```

## 主要流程

1. **文件上传**：用户上传 Markdown 文件
2. **文档加载**：用 UnstructuredMarkdownLoader 加载为 LangChain 文档对象
3. **文本切分**：用 RecursiveCharacterTextSplitter 切分为文本块
4. **向量化**：用 OpenAIEmbeddings 生成文本块向量
5. **索引构建**：用 FAISS 构建向量数据库
6. **问答链构建**：用 ChatOpenAI + RetrievalQA 构建检索增强问答链
7. **语义检索与问答**：用户输入问题，系统自动检索相关文本块并用 LLM 生成答案

## 关键模块说明

- **app_langchain.py**：主入口，负责 UI、参数配置、流程调度
- **modules/langchain_helper.py**：LangChain 相关功能的封装，便于维护和扩展
- **FAISS**：高效的本地向量数据库，支持大规模知识块检索
- **OpenAIEmbeddings/ChatOpenAI**：支持官方和第三方 API，兼容性强

## 会话状态管理

- `st.session_state.vectorstore`：FAISS 向量索引对象
- `st.session_state.qa_chain`：问答链对象
- `st.session_state.file_processed`：文件处理状态
- `st.session_state.openai_key`/`api_base`：API 配置

## 扩展性

- 支持多种文档格式（可扩展更多 Loader）
- 支持多种 LLM（可替换 ChatOpenAI）
- 支持多种向量数据库（可替换 FAISS）
- 便于集成更多 LangChain 工具链

## 性能与安全

- 本地向量索引，检索高效
- API Key 仅保存在本地 session，不落盘
- 支持大文件分块处理，适合个人/团队知识库

## 结语

本项目采用 LangChain 生态，极大提升了可扩展性和工程规范，适合二次开发和大规模知识库场景。
