# 个人知识库助手 - 开发者指南（LangChain 版）

## 环境准备

1. Python 3.8+
2. 推荐使用虚拟环境
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   pip install -U langchain-community
   ```

## 主要依赖
- streamlit
- langchain
- langchain-community
- faiss-cpu
- openai
- unstructured, unstructured-markdown

## 代码结构

```
md_helper/
├── app_langchain.py         # 主入口（推荐）
├── modules/
│   ├── langchain_helper.py  # LangChain 封装
│   └── ...                  # 其他兼容模块
├── docs/                    # 文档
```

## 开发建议

- 推荐所有新功能基于 langchain_helper.py 封装
- 文档加载/切分/嵌入/索引/问答链均可用 LangChain 生态扩展
- 支持自定义 LLM、向量数据库、文档格式
- 参考 LangChain 官方文档：https://python.langchain.com/

## 常见扩展点

- 支持 PDF/HTML/Docx 等更多 Loader
- 替换 LLM（如 Azure、Qwen、ChatGLM 等）
- 持久化 FAISS 索引到本地磁盘
- 多用户/多知识库支持

## 测试建议

- 推荐用 Streamlit 交互式测试
- 可用 pytest 对 langchain_helper.py 单元测试

## 贡献规范

- 遵循 PEP8
- 所有新模块建议写 docstring
- 重要变更请更新 docs/ 下相关文档

## 结语

本项目已全面集成 LangChain，开发者可专注于业务逻辑和链路创新，欢迎贡献更多插件和扩展！
