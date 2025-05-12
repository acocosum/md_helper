from typing import List

def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    将文本切分成固定大小的块，保持一定的重叠度以保留上下文
    
    Args:
        text (str): 要切分的文本
        chunk_size (int): 每个文本块的大小（字符数）
        overlap (int): 相邻块之间的重叠字符数
        
    Returns:
        List[str]: 切分后的文本块列表
    """
    # 如果文本长度小于块大小，直接返回
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    # 按照段落分割文本
    paragraphs = text.split('\n\n')
    current_chunk = ""
    
    for paragraph in paragraphs:
        # 如果段落加上当前块会超过块大小，则先保存当前块
        if len(current_chunk) + len(paragraph) + 2 > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # 重叠部分：取当前块的后overlap个字符
            # 如果当前块不足overlap长度，则全部保留
            overlap_size = min(overlap, len(current_chunk))
            current_chunk = current_chunk[-overlap_size:] if overlap_size > 0 else ""
        
        # 添加段落到当前块
        if current_chunk:
            current_chunk += "\n\n" + paragraph
        else:
            current_chunk = paragraph
    
    # 添加最后一个块
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # 特殊处理：如果块划分不合理（例如有非常长的段落），则使用字符直接切分
    if not chunks:
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]
    
    return chunks
