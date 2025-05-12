# 个人知识库助手 - 用户指南（LangChain 版）

## 1. 项目简介

本应用基于 Streamlit、LangChain、FAISS 和 OpenAI API/兼容API，支持上传 Markdown 文件，自动构建本地知识库并实现智能问答。

## 2. 快速上手

### 环境准备
- Python 3.8 及以上
- 安装依赖：
  ```bash
  pip install -r requirements.txt
  pip install -U langchain-community
  ```

### 启动应用
```bash
streamlit run app_langchain.py
```

### 基本流程
1. 在侧边栏输入 OpenAI API Key（或兼容API Key）
2. 如用第三方API，填写自定义API地址
3. 上传 Markdown 文件
4. 等待系统处理（自动切分、向量化、索引）
5. 在问答框输入问题，获取基于知识库的智能回答

## 3. 常见问题

- **API Key 无效/未初始化**：请检查 API Key 和 API 地址
- **401/404 错误**：API Key 或 API 地址错误，或目标API不支持 embedding/chat
- **大文件处理慢**：建议分块上传或增大 chunk_size
- **支持哪些文档格式？**：当前主推 Markdown，后续可扩展 PDF/HTML/Docx

## 4. 高级用法

- 支持自定义 chunk_size、chunk_overlap、检索数量等参数
- 支持自定义 API 地址，兼容大部分 OpenAI 生态 API
- 支持多轮问答（上下文可扩展）
- 支持本地知识库持久化（开发中）

## 5. 技术亮点

- 全流程基于 LangChain 封装，易于扩展
- 本地 FAISS 向量索引，检索高效
- 支持多种 LLM 和向量数据库扩展

## 6. 联系与反馈

- 如遇问题请提交 issue 或 PR
- 欢迎贡献新功能和文档

---

本项目适合个人/团队本地知识库智能问答，支持自定义 API 和多种扩展。
