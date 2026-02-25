# Designed by Wcowin
import re
from functools import lru_cache

# 预编译正则表达式（保持原有格式）
# 在这里排除不需要统计的文件：
EXCLUDE_PATTERNS = [
    re.compile(r'^index\.md$'),
    re.compile(r'^about/'),
    re.compile(r'^trip/index\.md$'),
    re.compile(r'^relax/index\.md$'),
    re.compile(r'^blog/indexblog\.md$'),
    re.compile(r'^blog/posts\.md$'),
    re.compile(r'^develop/index\.md$'),
    re.compile(r'waline\.md$'),
    re.compile(r'link\.md$'),
    re.compile(r'404\.md$'),
]

# 优化的字符统计正则表达式
CHINESE_CHARS_PATTERN = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
CODE_BLOCK_PATTERN = re.compile(r'```.*?```', re.DOTALL)
INLINE_CODE_PATTERN = re.compile(r'`[^`]+`')
YAML_FRONT_PATTERN = re.compile(r'^---.*?---\s*', re.DOTALL)
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
SCRIPT_TAG_PATTERN = re.compile(r'<script.*?>.*?</script>', re.DOTALL)
STYLE_TAG_PATTERN = re.compile(r'<style.*?>.*?</style>', re.DOTALL)
IMAGE_PATTERN = re.compile(r'!\[.*?\]\([^)]+\)')
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\([^)]+\)')

# 预定义排除类型
EXCLUDE_TYPES = frozenset({'landing', 'special', 'widget'})

# 扩展非编程行内代码词汇（更全面的过滤）
NON_CODE_WORDS = frozenset({
    'markdown', 'target', 'blank', 'lg', 'middle', 'small', 'large',
    'left', 'right', 'center', 'top', 'bottom', 'primary', 'secondary',
    'success', 'warning', 'danger', 'info', 'light', 'dark', 'grid',
    'cards', 'octicons', 'bookmark', 'div', 'class', 'img', 'src',
    'alt', 'width', 'height', 'style', 'id', 'data', 'href', 'title'
})

# 支持的编程和标记语言（扩展版本）
PROGRAMMING_LANGUAGES = frozenset({
    # 编程语言
    'python', 'py', 'javascript', 'js', 'typescript', 'ts', 'java', 'cpp', 'c', 
    'go', 'rust', 'php', 'ruby', 'swift', 'kotlin', 'csharp', 'cs',
    # 脚本语言
    'bash', 'sh', 'powershell', 'ps1', 'zsh', 'fish', 'bat', 'cmd',
    # 标记和配置语言
    'html', 'css', 'scss', 'sass', 'less', 'yaml', 'yml', 'json', 'xml',
    'toml', 'ini', 'conf', 'dockerfile', 'makefile',
    # 数据库和查询
    'sql', 'mysql', 'postgresql', 'sqlite', 'mongodb',
    # 其他
    'r', 'matlab', 'scala', 'perl', 'lua', 'dart', 'tex', 'latex',
    # 数据格式
    'csv', 'properties',
    # 无标识符（空字符串也算作有效语言）
    ''
})

@lru_cache(maxsize=256)
def clean_markdown_content_for_chinese(content_hash, markdown):
    """清理Markdown内容，只保留中文文本用于统计（添加缓存）"""
    content = markdown
    
    # 使用预编译的正则表达式（调整处理顺序，优先清理脚本和样式）
    content = YAML_FRONT_PATTERN.sub('', content)
    content = SCRIPT_TAG_PATTERN.sub('', content)
    content = STYLE_TAG_PATTERN.sub('', content)
    content = HTML_TAG_PATTERN.sub('', content)
    content = IMAGE_PATTERN.sub('', content)
    content = LINK_PATTERN.sub(r'\1', content)
    content = CODE_BLOCK_PATTERN.sub('', content)
    content = INLINE_CODE_PATTERN.sub('', content)
    
    return content

def count_code_lines(markdown):
    """统计代码行数（修复版本 - 正确处理所有代码行）"""
    code_blocks = CODE_BLOCK_PATTERN.findall(markdown)
    total_code_lines = 0
    
    for i, block in enumerate(code_blocks):
        # 提取语言标识
        lang_match = re.match(r'^```(\w*)', block)
        language = lang_match.group(1).lower() if lang_match else ''
        
        # 移除开头的语言标识和结尾的```
        code_content = re.sub(r'^```\w*\n?', '', block)
        code_content = re.sub(r'\n?```$', '', code_content)
        
        # 过滤空代码块
        if not code_content.strip():
            continue
        
        # 计算有效行数（包含所有非空行，包括注释行）
        lines = [line for line in code_content.split('\n') if line.strip()]
        line_count = len(lines)
        
        # 如果有明确的编程语言标识，直接统计
        if language and language in PROGRAMMING_LANGUAGES:
            total_code_lines += line_count
            continue
        
        # 增强的检测策略 - 更宽松的判断
        is_code = False
        
        # 1. 命令行检测
        command_indicators = [
            'sudo ', 'npm ', 'pip ', 'git ', 'cd ', 'ls ', 'mkdir ', 'rm ', 'cp ', 'mv ',
            'chmod ', 'chown ', 'grep ', 'find ', 'ps ', 'kill ', 'top ', 'cat ', 'echo ',
            'wget ', 'curl ', 'tar ', 'zip ', 'unzip ', 'ssh ', 'scp ', 'rsync ',
            'xattr ', 'codesign ', 'xcode-select ', 'spctl ', 'launchctl ',
            'brew ', 'defaults ', 'ditto ', 'hdiutil ', 'diskutil ',
            'dir ', 'copy ', 'xcopy ', 'del ', 'rd ', 'md ', 'type ', 'attrib ',
            '$ ', '# ', '% ', '> ', 'C:\\>', 'PS>',
            '--', '-r', '-d', '-f', '-v', '-h', '--help', '--version',
            '--force', '--deep', '--sign', '--master-disable',
            '/Applications/', '/usr/', '/etc/', '/var/', '/home/', '~/',
            'C:\\', 'D:\\', '.app', '.exe', '.pkg', '.dmg', '.zip', '.tar',
            '#!/',
        ]
        
        if any(indicator in code_content for indicator in command_indicators):
            is_code = True
        
        # 2. 编程语法检测（增强版）
        if not is_code:
            programming_indicators = [
                # Python语法特征
                'def ', 'class ', 'import ', 'from ', 'return ', 'yield ', 'lambda ',
                'with ', 'as ', 'try:', 'except:', 'finally:', 'elif ', 'if __name__',
                'print(', '.append(', '.extend(', '.remove(', '.sort(', '.reverse(',
                'range(', 'len(', 'str(', 'int(', 'float(', 'list(', 'dict(',
                # JavaScript/TypeScript语法
                'function', 'var ', 'let ', 'const ', 'async ', 'await ', '=>',
                'console.log', 'document.', 'window.', 'require(',
                # 通用编程语法
                'public ', 'private ', 'protected ', 'static ', 'void ', 'int ',
                'string ', 'boolean ', 'float ', 'double ', 'char ',
                # 操作符和结构
                '==', '!=', '<=', '>=', '&&', '||', '++', '--', '+=', '-=', '**',
                # 特殊结构
                'while ', 'for ', 'if ', 'else:', 'switch ', 'case ',
                # HTML/XML语法
                '<!DOCTYPE', '<html', '<head', '<body', '<div', '<span', '<p>',
                '<style', '<script', '<link', '<meta', '<title', '<img',
                # CSS语法
                'display:', 'color:', 'background:', 'margin:', 'padding:',
                'font-size:', 'width:', 'height:', 'position:', 'border:',
                # YAML语法
                'name:', 'version:', 'theme:', 'title:', 'description:',
                # JSON语法
                '{"', '"}', '":', '",', '[{', '}]', 'null', 'true', 'false',
                # 配置文件语法
                '[', ']', '//', '/*', '*/', '<!--', '-->',
                # SQL语法
                'SELECT ', 'FROM ', 'WHERE ', 'INSERT ', 'UPDATE ', 'DELETE ',
                'CREATE ', 'ALTER ', 'DROP ', 'INDEX ', 'TABLE ',
                # 数学公式和LaTeX
                '\\', '$', '$$', '\\begin', '\\end', '\\frac', '\\sum',
            ]
            
            if any(indicator in code_content for indicator in programming_indicators):
                is_code = True
        
        # 3. 结构化检测
        if not is_code:
            # 缩进结构检测
            if len(lines) > 1 and any(line.startswith('  ') or line.startswith('\t') for line in lines):
                is_code = True
            
            # HTML标签结构
            elif '<' in code_content and '>' in code_content:
                is_code = True
            
            # 包含特殊字符组合
            elif any(char in code_content for char in ['{', '}', '(', ')', '[', ']']) and ('=' in code_content or ':' in code_content):
                is_code = True
        
        # 4. 模式匹配检测（宽松策略）
        if not is_code and len(lines) >= 1:
            special_patterns = [
                r'\w+\(\)', r'\w+\[\]', r'\w+\{\}', r'\w+=\w+', r'\w+:\w+',
                r'<\w+>', r'\$\w+', r'#\w+', r'@\w+', r'\w+\.\w+\(\)',
                r'\d+\.\d+\.\d+', r'http[s]?://', r'ftp://', r'localhost',
                r'def\s+\w+', r'class\s+\w+', r'import\s+\w+', r'from\s+\w+',
                r'if\s+\w+', r'while\s+\w+', r'for\s+\w+', r'return\s+\w*',
                r'\w+\s*=\s*\w+', r'\w+\.\w+', r'#.*输出', r'#.*结果'
            ]
            
            if any(re.search(pattern, code_content) for pattern in special_patterns):
                is_code = True
        
        # 如果判断为代码，则统计行数
        if is_code:
            total_code_lines += line_count
    
    return total_code_lines

def calculate_reading_stats(markdown):
    """计算中文字符数和代码行数"""
    # 生成内容哈希用于缓存
    content_hash = hash(markdown)
    
    # 使用缓存的清理函数
    clean_content = clean_markdown_content_for_chinese(content_hash, markdown)
    chinese_chars = len(CHINESE_CHARS_PATTERN.findall(clean_content))
    
    # 统计代码行数
    code_lines = count_code_lines(markdown)
    
    # 计算阅读时间（中文：400字/分钟）
    reading_time = max(1, round(chinese_chars / 400))
    
    return reading_time, chinese_chars, code_lines

def on_page_markdown(markdown, **kwargs):
    page = kwargs['page']

    # 快速排除检查
    if page.meta.get('hide_reading_time', False):
        return markdown

    # 保持原有的EXCLUDE_PATTERNS循环检查方式
    src_path = page.file.src_path
    for pattern in EXCLUDE_PATTERNS:
        if pattern.match(src_path):
            return markdown

    # 优化类型检查
    page_type = page.meta.get('type', '')
    if page_type in EXCLUDE_TYPES:
        return markdown

    # 快速预检查，如果内容长度小于300字符，则不添加阅读信息
    if len(markdown) < 300:
        return markdown

    # 计算统计信息
    reading_time, chinese_chars, code_lines = calculate_reading_stats(markdown)

    # 生成阅读信息
    if code_lines > 0:
        reading_info = f"""<div markdown="1" style="margin-top: -30px; font-size: 0.80em; opacity: 0.7;">
:material-circle-edit-outline: 约 {chinese_chars} 个中文字符 :fontawesome-solid-code: {code_lines} 行代码 :material-clock-time-two-outline: 预计阅读时间 {reading_time} 分钟
</div>
"""
    else:
        reading_info = f"""<div markdown="1" style="margin-top: -30px; font-size: 0.80em; opacity: 0.7;">
:material-circle-edit-outline: 约 {chinese_chars} 个中文字符 :material-clock-time-two-outline: 预计阅读时间 {reading_time} 分钟
</div>
"""

    # 查找并插入到文档的第一个一级标题之后（保持标题为第一行）
    modified_content = re.sub(
        r'(^# .+?$)\n',
        rf'\1\n\n{reading_info}',
        markdown,
        count=1,
        flags=re.MULTILINE
    )

    # 如果没有找到一级标题，则在文档开头添加
    if modified_content == markdown:
        modified_content = f"{reading_info}\n\n{markdown}"

    return modified_content