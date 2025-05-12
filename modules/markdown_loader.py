import markdown
import io

def load_markdown(file) -> str:
    """
    加载并解析Markdown文件，返回纯文本内容
    
    Args:
        file: 上传的Markdown文件对象
        
    Returns:
        str: 提取的纯文本内容
    """
    # 读取文件内容
    if hasattr(file, 'read'):
        content = file.read().decode('utf-8')
    else:
        # 如果是文件路径而非文件对象
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
    
    # 将Markdown转换为HTML（这一步是为了处理链接、强调等Markdown语法）
    html = markdown.markdown(content)
    
    # 简单处理HTML标签，保留基本结构（如标题、段落）
    # 这里可以使用更复杂的HTML解析库如BeautifulSoup，但为简化依赖，我们用简单字符串处理
    text = html
    
    # 替换常见HTML标签为纯文本格式
    replacements = [
        ('<h1>', '# '), ('<h2>', '## '), ('<h3>', '### '),
        ('<h4>', '#### '), ('<h5>', '##### '), ('<h6>', '###### '),
        ('</h1>', '\n\n'), ('</h2>', '\n\n'), ('</h3>', '\n\n'),
        ('</h4>', '\n\n'), ('</h5>', '\n\n'), ('</h6>', '\n\n'),
        ('<p>', ''), ('</p>', '\n\n'),
        ('<ul>', '\n'), ('</ul>', '\n'), ('<ol>', '\n'), ('</ol>', '\n'),
        ('<li>', '- '), ('</li>', '\n'),
        ('<br>', '\n'), ('<br/>', '\n'), ('<br />', '\n'),
        ('<em>', '*'), ('</em>', '*'),
        ('<strong>', '**'), ('</strong>', '**'),
        ('<code>', '`'), ('</code>', '`')
    ]
    
    for old, new in replacements:
        text = text.replace(old, new)
    
    # 处理其他HTML标签
    in_tag = False
    result = io.StringIO()
    
    for char in text:
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
            continue
        elif not in_tag:
            result.write(char)
    
    # 处理连续空行，将多个空行替换为两个空行
    clean_text = '\n'.join([line for line in result.getvalue().split('\n') if line.strip()])
    
    return clean_text
