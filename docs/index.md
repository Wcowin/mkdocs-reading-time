---
title: MkDocs Reading Time
hide:
#   - navigation # 显示右
#   - toc #显示左
  - footer
  - feedback
comments: false
---  

<!-- # MkDocs Reading Time -->

<p align="center">
    <img src="https://img.shields.io/badge/MkDocs-reading_time-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white" alt="MkDocs Hooks">
    <!-- <img src="https://img.shields.io/badge/AI_Powered-DeepSeek-FF6B35?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered"> -->
    <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7+">
</p>


🌟**为MkDocs文档添加阅读时间统计功能！**     

支持自定义统计格式和排除特定页面,可计算中文字符数、代码行数并估算阅读时间，适用于长文档网站，提升用户体验。配置包含排除规则设置和本地预览测试方法，便于灵活部署。  

![image](https://s1.imagehub.cc/images/2025/06/06/a4584dbad4da3f87eb5c2f1e7ed14a74.png)

🌐 **在线演示**: https://wcowin.work/mkdocs-reading-time/

---

## 1. 基础配置

### **步骤1**    

下载[reading_time.py](https://github.com/Wcowin/mkdocs-reading-time/releases)


### **步骤2**

把reading_time.py放到docs/overrides/hooks目录下，然后在mkdocs.yml中添加：  

```yaml
# 在 mkdocs.yml 中添加
hooks:
  - docs/overrides/hooks/reading_time.py    # 阅读时间统计
```

### **步骤3**  
配置MkDocs主题以及覆写路径custom_dir
```yaml
# 在 mkdocs.yml 中添加
theme:
  name: material
  custom_dir: docs/overrides  # 必需配置！！！
  features:
    - content.code.copy
    - content.code.select
```

到这里检查下目录树状图:
```
$ tree -a
文件名
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

### **步骤4**

```bash
mkdocs serve  # 本地预览
```


## 2. 效果展示

![image](https://s1.imagehub.cc/images/2025/06/06/a4584dbad4da3f87eb5c2f1e7ed14a74.png)


## 3.高级配置

### 3.1 排除特定页面
如果有一些页面不想统计阅读时间，可以在页面的元数据中添加 `hide_reading_time: true`。例如：  

```markdown
---
title: 不统计阅读时间的页面
hide_reading_time: true
---
```

或者直接在reading_time.py中添加：  
```python
# 你想排除的页面路径
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

### 3.2 自定义统计信息
如果需要自定义统计信息的格式，可以修改reading_time.py中的calculate_reading_stats函数。例如：
```python
def calculate_reading_stats(markdown):
    # 计算统计信息
    reading_time, chinese_chars, code_lines = calculate_reading_stats(markdown) 
    # 自定义统计信息格式
    if code_lines > 0:
        reading_info = f"""!!! info "📖 阅读信息"
    阅读时间：**{reading_time}** 分钟 | 中文字符：**{chinese_chars}** | 有效代码行数：**{code_lines}**
    """
    else:
        reading_info = f"""!!! info "📖 阅读信息"
    阅读时间：**{reading_time}** 分钟 | 中文字符：**{chinese_chars}**
    """
    return reading_info + markdown
```

## 🐛 问题反馈

遇到问题？请在 [Issues](https://github.com/Wcowin/mkdocs-ai-hooks/issues) 中反馈。

**反馈时请包含**：  

- MkDocs版本
- Python版本
- 完整错误信息
- 复现步骤
- 配置文件（去除敏感信息）

---

## 📄 许可证

本项目采用 [MIT License](https://github.com/Wcowin/mkdocs-reading-time/blob/main/LICENSE) 开源协议。

---

## 🙏 致谢

感谢以下项目和服务：    

- [MkDocs](https://www.mkdocs.org/) - 优秀的静态站点生成器  
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - 精美的主题  
- 所有贡献者和使用者

---

## 🔗 联系作者


### Telegram
<div align="center">

<a href="https://t.me/wecowin" target="_blank">
<img src="https://pica.zhimg.com/80/v2-d5876bc0c8c756ecbba8ff410ed29c14_1440w.webp" alt="Telegram" style="border-radius: 10px;" width="300px">
</a>
</div>

### 微信交流
<div align="center">
<img src="https://pic3.zhimg.com/80/v2-5ef3dde831c9d0a41fe35fabb0cb8784_1440w.webp" style="border-radius: 10px;" width="300px">

</div>

---

## ⭐Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Wcowin/mkdocs-reading-time&type=Date)](https://www.star-history.com/#Wcowin/mkdocs-reading-time&Date)

---

## ☕ 支持项目

<div align="center">

<a href="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" target="_blank">
<img src="https://s1.imagehub.cc/images/2025/05/11/36eb33bf18f9041667267605b6b99bd0.jpeg" style="width: 300px; border-radius: 15px;">
</a>


</div>

**如果这个项目对您有帮助，请给它一个 ⭐ Star！**

---



📝 *让MkDocs文档更加系统化*

**[⬆ 回到顶部](#1)**

