import numpy as np
from typing import List, Tuple

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    计算两个向量之间的余弦相似度
    
    Args:
        vec1 (List[float]): 第一个向量
        vec2 (List[float]): 第二个向量
        
    Returns:
        float: 余弦相似度，范围在[-1, 1]之间
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    # 计算点积
    dot_product = np.dot(vec1, vec2)
    
    # 计算向量范数
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    # 防止除以零
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
        
    # 计算余弦相似度
    similarity = dot_product / (norm_vec1 * norm_vec2)
    
    return similarity

def retrieve(query_embedding: List[float], doc_embeddings: List[List[float]], top_k: int = 3) -> List[int]:
    """
    检索与查询向量最相似的文档向量索引
    
    Args:
        query_embedding (List[float]): 查询的向量表示
        doc_embeddings (List[List[float]]): 文档向量列表
        top_k (int): 返回的最相似文档数量
        
    Returns:
        List[int]: 最相似的文档索引列表
    """
    # 如果文档向量为空，返回空列表
    if not doc_embeddings:
        return []
    
    # 计算查询向量与所有文档向量的相似度
    similarities = [cosine_similarity(query_embedding, doc_embedding) 
                   for doc_embedding in doc_embeddings]
    
    # 获取相似度排序后的索引
    sorted_indices = np.argsort(similarities)[::-1]  # 从大到小排序
    
    # 返回top_k个最相似的文档索引
    return sorted_indices[:min(top_k, len(sorted_indices))].tolist()
