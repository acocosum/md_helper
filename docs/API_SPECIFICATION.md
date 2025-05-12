# 个人知识库助手 - API 接口规范

本文档详细说明个人知识库助手系统中的关键API接口、数据结构和集成规范，主要针对希望了解系统内部工作原理或进行二次开发的开发者。

## OpenAI API 接口集成

### 向量嵌入 API (Embeddings)

#### 请求格式

```json
{
  "model": "text-embedding-ada-002",
  "input": "文本内容"
}
```

#### 响应格式

```json
{
  "data": [
    {
      "embedding": [0.0023064255, -0.009327292, ...], // 1536维向量
      "index": 0,
      "object": "embedding"
    }
  ],
  "model": "text-embedding-ada-002",
  "object": "list",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
```

#### 实际调用示例

```python
response = openai_client.embeddings.create(
    model="text-embedding-ada-002",
    input=text
)
embedding = response.data[0].embedding
```

### 聊天完成 API (Chat Completions)

#### 请求格式

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "你是一个智能知识库助手，根据提供的上下文回答用户问题。"
    },
    {
      "role": "user",
      "content": "基于以下上下文回答问题：\n\n上下文：...\n\n问题：..."
    }
  ],
  "temperature": 0.3,
  "max_tokens": 800
}
```

#### 响应格式

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677858242,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "这是回答内容..."
      },
      "index": 0,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 56,
    "completion_tokens": 31,
    "total_tokens": 87
  }
}
```

#### 实际调用示例

```python
response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是一个智能知识库助手，根据提供的上下文回答用户问题。"},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,
    max_tokens=800
)
answer = response.choices[0].message.content
```

## 内部模块 API

### markdown_loader 模块

#### load_markdown(file)

加载并解析Markdown文件，返回纯文本内容。

- **输入**: 
  - `file`: 文件对象或文件路径字符串
- **输出**: 
  - `str`: 提取的纯文本内容
- **处理流程**:
  1. 读取文件内容
  2. 将Markdown转换为HTML
  3. 处理HTML标签，保留基本结构（标题、段落等）
  4. 返回处理后的纯文本

### text_splitter 模块

#### split_text(text, chunk_size=500, overlap=50)

将文本切分成固定大小的块，保持一定的重叠度以保留上下文。

- **输入**:
  - `text`: 要切分的文本
  - `chunk_size`: 每个文本块的大小（默认500字符）
  - `overlap`: 相邻块之间的重叠字符数（默认50字符）
- **输出**:
  - `List[str]`: 切分后的文本块列表
- **处理流程**:
  1. 按段落分割文本
  2. 根据块大小和重叠度组合段落
  3. 处理边界情况（如超长段落）
  4. 返回文本块列表

### embedder 模块

#### initialize_openai(api_key, custom_api_base=None)

初始化OpenAI客户端。

- **输入**:
  - `api_key`: OpenAI API密钥
  - `custom_api_base`: 自定义API基础URL（默认None，使用官方API）
- **输出**: 
  - `None`: 设置全局openai_client和session状态
- **处理流程**:
  1. 处理API基础URL，去除端点路径
  2. 创建OpenAI客户端实例
  3. 存储客户端到session state中

#### get_embedding(text)

获取文本的向量表示。

- **输入**:
  - `text`: 需要向量化的文本内容
- **输出**:
  - `List[float]`: 1536维的向量表示
- **处理流程**:
  1. 调用OpenAI Embeddings API
  2. 提取并返回嵌入向量
  3. 错误处理（返回零向量以避免崩溃）

### retriever 模块

#### cosine_similarity(vec1, vec2)

计算两个向量之间的余弦相似度。

- **输入**:
  - `vec1`, `vec2`: 两个向量（浮点数列表）
- **输出**:
  - `float`: 余弦相似度值（范围-1到1）
- **处理流程**:
  1. 将列表转换为NumPy数组
  2. 计算点积和向量范数
  3. 返回余弦相似度

#### retrieve(query_embedding, doc_embeddings, top_k=3)

检索与查询向量最相似的文档向量索引。

- **输入**:
  - `query_embedding`: 查询文本的向量表示
  - `doc_embeddings`: 文档向量列表
  - `top_k`: 返回的最相似文档数量（默认3）
- **输出**:
  - `List[int]`: 最相似文档的索引列表
- **处理流程**:
  1. 计算查询向量与所有文档向量的相似度
  2. 对相似度进行降序排序
  3. 返回top_k个最相似文档的索引

### qa_chain_new 模块

#### generate_answer(question, context_chunks)

基于上下文生成问题的答案。

- **输入**:
  - `question`: 用户的问题
  - `context_chunks`: 相关的文本块列表
- **输出**:
  - `str`: 生成的答案
- **处理流程**:
  1. 从session状态获取OpenAI客户端
  2. 合并上下文文本块
  3. 构造提示内容（prompt）
  4. 调用OpenAI Chat API
  5. 提取并返回生成的答案

## 数据结构

### 文本块 (Chunks)

```python
chunks = [
    "这是第一个文本块，包含了文档的一部分内容...",
    "这是第二个文本块，包含了另一部分内容...",
    # ...更多文本块
]
```

- 存储在 `st.session_state.chunks`
- 类型为字符串列表
- 每个块大约包含chunk_size字符（除非是文档边界）

### 嵌入向量 (Embeddings)

```python
embeddings = [
    [0.002306, -0.009327, ...],  # 1536维向量
    [0.001826, 0.007281, ...],   # 1536维向量
    # ...更多向量
]
```

- 存储在 `st.session_state.embeddings`
- 类型为二维浮点数列表
- 每个向量与chunks中的相应文本块一一对应
- 使用OpenAI的text-embedding-ada-002模型，维度为1536

## 自定义API集成规范

要支持自定义API端点，该API服务必须兼容以下接口：

### 嵌入接口 (Embeddings)

- **端点**: `/embeddings` 或 基础URL + `/embeddings`
- **方法**: POST
- **请求格式**:
  ```json
  {
    "model": "text-embedding-ada-002",
    "input": "文本内容"
  }
  ```
- **响应格式**: 必须与OpenAI Embeddings API响应格式兼容
- **鉴权**: Bearer Token (API密钥)

### 聊天接口 (Chat)

- **端点**: `/chat/completions` 或 基础URL + `/chat/completions`
- **方法**: POST
- **请求格式**:
  ```json
  {
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."}
    ],
    "temperature": 0.3,
    "max_tokens": 800
  }
  ```
- **响应格式**: 必须与OpenAI Chat API响应格式兼容
- **鉴权**: Bearer Token (API密钥)

## 会话状态变量

项目使用Streamlit的会话状态(st.session_state)存储以下关键变量：

```python
# 文本块列表
st.session_state.chunks = []

# 嵌入向量列表
st.session_state.embeddings = []

# 文件处理状态标记
st.session_state.file_processed = False

# OpenAI API密钥
st.session_state.openai_key = ""

# 自定义API基础URL
st.session_state.api_base = ""

# OpenAI客户端实例
st.session_state.openai_client = None
```

## API调用错误处理

### 常见错误代码

| 错误代码 | 含义 | 处理方式 |
|---------|------|---------|
| 401     | 未授权 | 检查API密钥有效性 |
| 404     | 端点未找到 | 检查API URL格式和服务支持 |
| 429     | 速率限制 | 添加重试逻辑和延迟 |
| 500     | 服务器错误 | 提供友好错误信息并记录日志 |

### 错误处理示例

```python
try:
    # API调用代码
    response = openai_client.embeddings.create(...)
except Exception as e:
    error_message = str(e)
    if "401" in error_message:
        return "API认证失败，请检查您的API密钥"
    elif "404" in error_message:
        return "API端点未找到，请检查您的API地址是否支持嵌入功能"
    elif "429" in error_message:
        return "API请求频率过高，请稍后再试"
    else:
        return f"发生错误: {error_message}"
```

## 自定义扩展接口

以下是为扩展功能预留的接口规范：

### 自定义向量存储

```python
class VectorStore:
    def __init__(self, config=None):
        # 初始化向量存储
        pass
    
    def add(self, texts, embeddings):
        # 添加文本和向量到存储
        pass
    
    def search(self, query_embedding, top_k=3):
        # 搜索相似向量
        pass
    
    def save(self, path):
        # 保存向量存储到文件
        pass
    
    def load(self, path):
        # 从文件加载向量存储
        pass
```

### 自定义文档加载器

```python
class DocumentLoader:
    def __init__(self):
        # 初始化加载器
        pass
    
    def load(self, file):
        # 加载文档
        pass
    
    def supported_formats(self):
        # 返回支持的文档格式
        return [".md", ".txt", ...]
```

### 自定义LLM提供商

```python
class LLMProvider:
    def __init__(self, api_key, api_base=None):
        # 初始化LLM提供商
        pass
    
    def generate(self, prompt, max_tokens=800, temperature=0.3):
        # 生成回答
        pass
    
    def get_embeddings(self, text):
        # 获取文本嵌入
        pass
```

## API版本兼容性

本项目使用OpenAI Python SDK v1.0+，采用以下格式调用API：

```python
# 旧版本 (< 1.0)
# response = openai.Embedding.create(...)

# 新版本 (≥ 1.0)
response = openai_client.embeddings.create(...)
```

请确保您的自定义API实现或扩展与此版本兼容。如果使用旧版本的OpenAI SDK，需要相应调整代码。

## 安全性考量

### API密钥处理

- 使用Streamlit的密码输入框保护API密钥
- 仅保存在内存会话状态中
- 不写入配置文件或日志
- 不使用全局环境变量存储密钥

### 数据处理

- 上传的文档和生成的向量仅保存在内存中
- 应用关闭后数据自动清除
- 所有API调用使用HTTPS加密传输数据

## 结语

本文档提供了个人知识库助手项目的API和接口规范，开发者可以基于此进行功能扩展或二次开发。如有任何问题或建议，欢迎贡献代码或提出issues。
