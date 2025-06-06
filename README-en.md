# MkDocs Reading Time

<p align="center">
    <img src="https://img.shields.io/badge/MkDocs-reading time-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white" alt="MkDocs Hooks">
    <!-- <img src="https://img.shields.io/badge/AI_Powered-DeepSeek-FF6B35?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered"> -->
    <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7+">
</p>

<p align="center">
    <a href="README.md">中文</a> | <a href="README-en.md">English</a>
</p>

🌟**Add reading time statistics feature to MkDocs documentation!**     

Supports custom statistics format and excluding specific pages. It can calculate Chinese character count, code lines, and estimate reading time, suitable for long documentation websites to enhance user experience. Configuration includes exclusion rule settings and local preview testing methods for flexible deployment.

![image](https://s1.imagehub.cc/images/2025/06/06/a4584dbad4da3f87eb5c2f1e7ed14a74.png)

🌐 **Live Demo**: https://wcowin.work/mkdocs-reading-time/

---

## 1. Basic Configuration

### **Step 1**    

Download [reading_time.py](https://github.com/Wcowin/mkdocs-reading-time/releases)

### **Step 2**

Place reading_time.py in the docs/overrides/hooks directory, then add to mkdocs.yml:

```yaml
# Add to mkdocs.yml
hooks:
  - docs/overrides/hooks/reading_time.py    # Reading time statistics
```

### **Step 3**  
Configure MkDocs theme and custom_dir override path
```yaml
# Add to mkdocs.yml
theme:
  name: material
  custom_dir: docs/overrides  # Required configuration!!!
  features:
    - content.code.copy
    - content.code.select
```

Check the directory tree structure here:
```
$ tree -a
filename
├── .github
│   ├── .DS_Store
│   └── workflows
│       └── ci.yml
├── docs
│   └── index.md
|   └── overrides
│       └── hooks
│           └── reading_time.py
│           └── ...
└── mkdocs.yml
```

### **Step 4**

```bash
mkdocs serve  # Local preview
```

## 2. Effect Display

![image](https://s1.imagehub.cc/images/2025/06/06/a4584dbad4da3f87eb5c2f1e7ed14a74.png)

## 3. Advanced Configuration

### 3.1 Exclude Specific Pages
If you don't want to count reading time for some pages, you can add `hide_reading_time: true` to the page metadata. For example:

```markdown
---
title: Page without reading time statistics
hide_reading_time: true
---
```

Or add directly in reading_time.py:
```python
# Page paths you want to exclude
EXCLUDE_PATTERNS = [
    re.compile(r'^index\.md$'),
    re.compile(r'^trip/index\.md$'),
    re.compile(r'^relax/index\.md$'),
    re.compile(r'^blog/indexblog\.md$'),
    re.compile(r'^blog/posts\.md$'),
    re.compile(r'^develop/index\.md$'),
    re.compile(r'waline\.md$'),
    re.compile(r'link\.md$'),
    re.compile(r'404\.md$'),
]
``` 

### 3.2 Custom Statistics Information
If you need to customize the format of statistics information, you can modify the calculate_reading_stats function in reading_time.py. For example:
```python
def calculate_reading_stats(markdown):
    # Calculate statistics
    reading_time, chinese_chars, code_lines = calculate_reading_stats(markdown) 
    # Custom statistics format
    if code_lines > 0:
        reading_info = f"""!!! info "📖 Reading Information"
    Reading Time: **{reading_time}** minutes | Chinese Characters: **{chinese_chars}** | Effective Code Lines: **{code_lines}**
    """
    else:
        reading_info = f"""!!! info "📖 Reading Information"
    Reading Time: **{reading_time}** minutes | Chinese Characters: **{chinese_chars}**
    """
    return reading_info + markdown
```

## 🐛 Issue Feedback

Encountered problems? Please provide feedback in [Issues](https://github.com/Wcowin/mkdocs-ai-hooks/issues).

**Please include when reporting**：
- MkDocs version
- Python version
- Complete error message
- Steps to reproduce
- Configuration files (remove sensitive information)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) open source license.

---

## 🙏 Acknowledgments

Thanks to the following projects and services:
- [MkDocs](https://www.mkdocs.org/) - Excellent static site generator
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - Beautiful theme
- All contributors and users

---

## 🔗 Contact Author

<div align="center">

### Telegram
<a href="https://t.me/wecowin" target="_blank">
<img src="https://pica.zhimg.com/80/v2-d5876bc0c8c756ecbba8ff410ed29c14_1440w.webp" alt="Telegram" style="border-radius: 10px;" width="300px">
</a>

### WeChat Communication
<img src="https://pic3.zhimg.com/80/v2-5ef3dde831c9d0a41fe35fabb0cb8784_1440w.webp" style="border-radius: 10px;" width="300px">

</div>

---

## ⭐ Project Statistics

<div align="center">

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Wcowin/mkdocs-reading-time&type=Date)](https://www.star-history.com/#Wcowin/mkdocs-reading-time&Date)

</div>

---

## ☕ Support Project

<div align="center">

<a href="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" target="_blank">
<img src="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" style="width: 300px; border-radius: 15px;">
</a>

**If this project helps you, please give it a ⭐ Star!**

</div>

---

<div align="center">

📝 *Make MkDocs documentation more systematic*

**[⬆ Back to Top](#mkdocs-reading-time)**

</div>
