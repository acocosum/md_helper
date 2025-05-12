# 个人知识库助手 - 开发者指南

本文档为希望参与个人知识库助手项目开发、扩展或自定义功能的开发者提供指南。

## 环境搭建

### 开发环境准备

1. 克隆仓库并创建虚拟环境：

```bash
# 克隆仓库
git clone https://github.com/yourusername/md_helper.git
cd md_helper

# 创建虚拟环境
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 启动开发服务器：

```bash
streamlit run app.py
```

### 推荐的开发工具

- **编辑器/IDE**: Visual Studio Code 或 PyCharm
- **版本控制**: Git
- **代码格式化**: Black、isort
- **代码检查**: Pylint 或 Flake8
- **API 测试**: Postman 或 curl

## 代码组织

```
md_helper/
├── app.py                     # 主应用程序入口
├── modules/                   # 核心功能模块
│   ├── embedder.py            # 向量嵌入功能
│   ├── markdown_loader.py     # Markdown 文件处理
│   ├── qa_chain_new.py        # 问答链实现
│   ├── retriever.py           # 向量检索功能
│   └── text_splitter.py       # 文本切分功能
├── docs/                      # 文档目录
│   ├── PROJECT_ARCHITECTURE.md # 项目架构文档
│   └── DEVELOPER_GUIDE.md     # 开发者指南(本文档)
├── requirements.txt           # 项目依赖
└── README.md                  # 项目概述
```

## 核心模块开发指南

### 主应用程序 (app.py)

主应用程序负责用户界面和工作流程协调。修改这个文件时，请注意：

- 保持 Streamlit 组件的逻辑排列
- 会话状态（`st.session_state`）存储关键数据
- 对用户体验的影响（加载状态、错误处理等）

扩展建议：
- 添加文件批量上传功能
- 实现知识库保存与加载
- 添加更多自定义选项（如模型选择）

### Markdown 加载器 (markdown_loader.py)

负责解析和提取 Markdown 文件内容。改进方向：

- 增强 HTML 到纯文本的转换逻辑
- 添加对表格、代码块等特殊元素的处理
- 支持更多文档格式（如 HTML、PDF、DOC 等）

示例扩展 - 添加表格支持：

```python
def process_tables(html_content):
    """处理HTML中的表格，将其转换为Markdown格式表格"""
    # 实现表格解析逻辑
    pass
```

### 文本分割器 (text_splitter.py)

负责将长文本分割成短块。开发重点：

- 平衡块大小和语义完整性
- 考虑特定语言/领域的分割规则
- 实现更智能的分割策略（如基于语义边界）

示例扩展 - 智能段落分割：

```python
def smart_split_paragraphs(text, language="zh"):
    """根据语言特性智能分割段落"""
    # 实现基于语言规则的分割逻辑
    pass
```

### 向量嵌入器 (embedder.py)

处理文本向量化功能。扩展方向：

- 支持更多嵌入模型（如本地模型）
- 添加向量缓存机制减少API调用
- 实现批量嵌入以提高效率

示例扩展 - 添加向量缓存：

```python
def get_embedding_with_cache(text, cache_file="embedding_cache.pkl"):
    """使用本地缓存获取嵌入向量"""
    # 实现缓存检查和存储逻辑
    pass
```

### 向量检索器 (retriever.py)

实现相似度搜索。改进空间：

- 实现更高级的相似度算法
- 添加预过滤逻辑提高检索速度
- 集成向量数据库（如FAISS、Milvus等）

示例扩展 - 集成FAISS：

```python
def faiss_retriever(query_vector, document_vectors, top_k=3):
    """使用FAISS进行高效向量检索"""
    # 实现FAISS索引和检索逻辑
    pass
```

### 问答链 (qa_chain_new.py)

负责最终问答生成。开发重点：

- 优化提示工程（prompt engineering）
- 支持不同的LLM模型和参数设置
- 实现回答质量评估机制

示例扩展 - 添加模型参数配置：

```python
def generate_answer_with_params(question, context_chunks, 
                               model="gpt-3.5-turbo", 
                               temperature=0.3, 
                               max_tokens=800):
    """使用可配置参数生成答案"""
    # 实现动态模型和参数选择
    pass
```

## 高级功能开发

### 向量数据库集成

对于大型知识库，建议集成专门的向量数据库：

```python
def setup_vector_db(embeddings, chunks, db_type="chroma"):
    """初始化向量数据库"""
    if db_type == "chroma":
        # 设置ChromaDB
        pass
    elif db_type == "faiss":
        # 设置FAISS
        pass
    # 返回数据库连接
```

### 知识库持久化

实现知识库的保存和加载功能：

```python
def save_knowledge_base(chunks, embeddings, filename="knowledge_base"):
    """保存知识库到文件"""
    import pickle
    data = {"chunks": chunks, "embeddings": embeddings}
    with open(f"{filename}.pkl", "wb") as f:
        pickle.dump(data, f)

def load_knowledge_base(filename="knowledge_base"):
    """从文件加载知识库"""
    import pickle
    try:
        with open(f"{filename}.pkl", "rb") as f:
            data = pickle.load(f)
        return data["chunks"], data["embeddings"]
    except FileNotFoundError:
        return [], []
```

### 多模型支持

扩展程序以支持多种语言模型：

```python
def get_llm_client(provider="openai", model_name=None, api_key=None, api_base=None):
    """获取不同提供商的语言模型客户端"""
    if provider == "openai":
        # 返回OpenAI客户端
        pass
    elif provider == "anthropic":
        # 返回Anthropic客户端
        pass
    elif provider == "local":
        # 返回本地模型客户端
        pass
```

### 自定义文本处理流水线

为特定领域定制文本处理流程：

```python
class TextProcessingPipeline:
    """可定制的文本处理流水线"""
    
    def __init__(self):
        self.steps = []
        
    def add_step(self, step_func):
        """添加处理步骤"""
        self.steps.append(step_func)
        
    def process(self, text):
        """执行整个处理流程"""
        result = text
        for step in self.steps:
            result = step(result)
        return result
```

## 测试指南

### 单元测试

项目应包含针对各模块的单元测试。创建`tests`目录并为每个模块编写测试：

```python
# tests/test_embedder.py
import unittest
from modules.embedder import get_embedding

class TestEmbedder(unittest.TestCase):
    def test_get_embedding(self):
        # 使用mock模拟API调用
        text = "测试文本"
        # 编写测试逻辑
```

### 集成测试

测试模块间的协作：

```python
# tests/test_integration.py
import unittest
from modules.markdown_loader import load_markdown
from modules.text_splitter import split_text
from modules.embedder import get_embedding

class TestIntegration(unittest.TestCase):
    def test_load_split_embed_pipeline(self):
        # 测试从加载到嵌入的完整流程
        pass
```

## 性能优化

### 减少API调用

通过批处理和缓存减少API调用：

```python
def batch_get_embeddings(texts, batch_size=20):
    """批量获取嵌入向量"""
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        # 批量处理嵌入
        batch_results = process_batch(batch)
        results.extend(batch_results)
    return results
```

### 向量计算优化

优化向量相似度计算：

```python
def optimized_cosine_similarity(query_vector, doc_vectors):
    """优化的余弦相似度计算"""
    # 使用矩阵运算代替循环
    query_vector = np.array(query_vector).reshape(1, -1)
    doc_vectors = np.array(doc_vectors)
    
    # 计算点积
    dot_product = np.dot(query_vector, doc_vectors.T).flatten()
    
    # 计算范数
    query_norm = np.linalg.norm(query_vector)
    doc_norms = np.linalg.norm(doc_vectors, axis=1)
    
    # 计算相似度
    similarities = dot_product / (query_norm * doc_norms)
    
    return similarities
```

## 部署指南

### Docker部署

创建Dockerfile简化部署流程：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

构建和运行容器：

```bash
docker build -t md_helper .
docker run -p 8501:8501 md_helper
```

### 环境变量配置

使用环境变量管理敏感配置：

```python
# 在app.py中添加
import os

# 从环境变量获取默认API密钥
default_api_key = os.environ.get("OPENAI_API_KEY", "")
default_api_base = os.environ.get("OPENAI_API_BASE", "")

# 在界面中使用这些默认值
api_key = st.text_input("输入OpenAI API Key", type="password", value=default_api_key or st.session_state.openai_key)
```

## 贡献指南

### 提交代码

贡献代码时，请遵循这些步骤：

1. Fork仓库并克隆到本地
2. 创建新的分支：`git checkout -b feature/your-feature-name`
3. 编写代码和测试
4. 提交更改：`git commit -m "Add feature: description"`
5. 推送到远程：`git push origin feature/your-feature-name`
6. 创建Pull Request

### 代码规范

- 遵循PEP 8风格指南
- 为所有函数添加文档字符串（docstring）
- 保持代码的模块化和可测试性
- 使用类型注解提高代码可读性

### 文档更新

当添加或修改功能时，请更新相关文档：

- README.md中的功能列表和使用说明
- 新功能的详细文档
- 注释和函数文档字符串

## 常见问题与解决方案

### API连接问题

如果用户遇到API连接问题：

```python
def test_api_connection(api_key, api_base=None):
    """测试API连接是否正常"""
    try:
        # 尝试简单的API调用
        client = get_openai_client(api_key, api_base)
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input="测试连接"
        )
        return True, "API连接正常"
    except Exception as e:
        return False, f"API连接错误: {str(e)}"
```

### 内存使用优化

处理大型知识库时的内存优化：

```python
def process_large_file(file_path, chunk_size=1000):
    """分块处理大文件以减少内存使用"""
    # 实现渐进式文件处理逻辑
    pass
```

## 未来发展方向

### 短期目标

- 支持更多文档格式（PDF、DOCX等）
- 添加本地向量存储功能
- 改进文本切分算法

### 中期目标

- 实现增量更新知识库
- 添加用户认证和多用户支持
- 集成内置的本地LLM选项

### 长期愿景

- 开发知识库管理界面
- 添加自动文档分类功能
- 实现跨知识库搜索和问答

## 结语

通过本指南，希望开发者能够更轻松地参与个人知识库助手项目的开发和扩展。无论是改进现有功能，还是添加全新特性，都欢迎提交贡献。项目的目标是打造一个易用、高效、可扩展的个人知识管理工具，帮助用户更好地组织和利用自己的知识资源。
