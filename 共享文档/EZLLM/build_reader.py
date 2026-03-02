import os
import json
import re

def build_site():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "docs")

    if not os.path.exists(docs_dir):
        print(f"Directory {docs_dir} does not exist. Creating it.")
        os.makedirs(docs_dir)

    documents = []

    # 遍历 docs 目录下的所有 txt 文件
    for filename in sorted(os.listdir(docs_dir)):
        if filename.endswith(".txt") and filename != "requirements.txt":
            file_path = os.path.join(docs_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 去除后缀作为标题
            title = os.path.splitext(filename)[0]

            # 提取文章中的小标题（以？结尾的行，或者特定格式）
            headings = []
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                # 匹配：以"什么是"开头、以？结尾、或者是短标题格式
                if line and (line.endswith('？') or line.endswith('?')) and len(line) < 30:
                    headings.append(line)
                elif line and re.match(r'^[①②③④⑤⑥⑦⑧⑨⑩❌✅]', line):
                    headings.append(line[:20] + ('...' if len(line) > 20 else ''))
                elif line and re.match(r'^(为什么|如何|怎么|通俗来说|说白了|举个例子)', line):
                    headings.append(line[:20] + ('...' if len(line) > 20 else ''))

            documents.append({
                "title": title,
                "content": content,
                "headings": headings[:8]  # 最多8个小标题
            })

    if not documents:
        print("未在 docs/ 目录下找到任何 .txt 文件。")

    js_data = json.dumps(documents, ensure_ascii=False)

    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EZLLM - 零基础学大模型</title>
    <meta name="description" content="从入门到精通，用最通俗的语言讲解 AI 大语言模型">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f6f6f7;
            --bg-sidebar: #f6f6f7;
            --text-primary: #1a1a1a;
            --text-secondary: #666666;
            --text-muted: #999999;
            --border-color: #e2e2e3;
            --accent: #5672cd;
            --accent-light: #eef1fa;
            --accent-hover: #4861b3;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
            --radius-sm: 6px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --sidebar-width: 280px;
            --toc-width: 220px;
            --header-height: 64px;
            --transition: all 0.2s ease;
        }

        [data-theme="dark"] {
            --bg-primary: #1a1a1a;
            --bg-secondary: #242424;
            --bg-sidebar: #161616;
            --text-primary: #ffffff;
            --text-secondary: #a8a8a8;
            --text-muted: #666666;
            --border-color: #2e2e2e;
            --accent: #6b8aff;
            --accent-light: #2a2f42;
            --accent-hover: #8ba3ff;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.2);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: var(--transition);
        }

        /* 顶部导航栏 */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--header-height);
            background: var(--bg-primary);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            padding: 0 24px;
            z-index: 100;
            backdrop-filter: blur(12px);
            background: rgba(255,255,255,0.85);
        }

        [data-theme="dark"] .header {
            background: rgba(26,26,26,0.85);
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 32px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            font-weight: 700;
            font-size: 18px;
            color: var(--text-primary);
        }

        .logo i {
            font-size: 24px;
            color: var(--accent);
        }

        .header-nav {
            display: flex;
            gap: 8px;
        }

        .header-nav a {
            padding: 8px 16px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            border-radius: var(--radius-sm);
            transition: var(--transition);
        }

        .header-nav a:hover,
        .header-nav a.active {
            color: var(--accent);
            background: var(--accent-light);
        }

        .header-right {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 16px;
        }

        /* 搜索框 */
        .search-trigger {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 14px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            color: var(--text-muted);
            font-size: 14px;
            cursor: pointer;
            transition: var(--transition);
            min-width: 200px;
        }

        .search-trigger:hover {
            border-color: var(--accent);
        }

        .search-trigger kbd {
            margin-left: auto;
            padding: 2px 6px;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 12px;
            font-family: inherit;
        }

        /* 主题切换 */
        .theme-toggle {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            cursor: pointer;
            border-radius: var(--radius-sm);
            font-size: 20px;
            transition: var(--transition);
        }

        .theme-toggle:hover {
            background: var(--bg-secondary);
            color: var(--accent);
        }

        /* 主容器 */
        .container {
            display: flex;
            padding-top: var(--header-height);
            min-height: 100vh;
        }

        /* 侧边栏 */
        .sidebar {
            position: fixed;
            top: var(--header-height);
            left: 0;
            width: var(--sidebar-width);
            height: calc(100vh - var(--header-height));
            background: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            overflow-y: auto;
            padding: 24px 16px;
            z-index: 50;
        }

        .sidebar-section {
            margin-bottom: 24px;
        }

        .sidebar-title {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            padding: 0 12px;
            margin-bottom: 8px;
        }

        .nav-list {
            list-style: none;
        }

        .nav-item {
            margin-bottom: 2px;
        }

        .nav-link {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            border-radius: var(--radius-sm);
            transition: var(--transition);
            cursor: pointer;
        }

        .nav-link i {
            font-size: 16px;
            opacity: 0.7;
        }

        .nav-link:hover {
            background: var(--bg-primary);
            color: var(--text-primary);
        }

        .nav-link.active {
            background: var(--accent-light);
            color: var(--accent);
        }

        .nav-link.active i {
            opacity: 1;
        }

        /* 主内容区 */
        .main {
            flex: 1;
            margin-left: var(--sidebar-width);
            margin-right: var(--toc-width);
            min-width: 0;
        }

        /* Hero 首页区域 */
        .hero {
            padding: 80px 64px;
            text-align: center;
            background: linear-gradient(135deg, var(--accent-light) 0%, var(--bg-primary) 100%);
            border-bottom: 1px solid var(--border-color);
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: var(--accent);
            color: white;
            font-size: 12px;
            font-weight: 600;
            border-radius: 20px;
            margin-bottom: 24px;
        }

        .hero h1 {
            font-size: 48px;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 16px;
            background: linear-gradient(135deg, var(--accent) 0%, #9b6dff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero p {
            font-size: 20px;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 32px;
        }

        .hero-buttons {
            display: flex;
            gap: 12px;
            justify-content: center;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 28px;
            font-size: 15px;
            font-weight: 600;
            border-radius: var(--radius-md);
            text-decoration: none;
            transition: var(--transition);
            cursor: pointer;
            border: none;
        }

        .btn-primary {
            background: var(--accent);
            color: white;
        }

        .btn-primary:hover {
            background: var(--accent-hover);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(86,114,205,0.3);
        }

        .btn-secondary {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }

        .btn-secondary:hover {
            border-color: var(--accent);
            color: var(--accent);
        }

        /* 特性卡片 */
        .features {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            padding: 64px;
            max-width: 1100px;
            margin: 0 auto;
        }

        .feature-card {
            padding: 32px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            transition: var(--transition);
            cursor: pointer;
        }

        .feature-card:hover {
            border-color: var(--accent);
            transform: translateY(-4px);
            box-shadow: var(--shadow-md);
        }

        .feature-icon {
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--accent-light);
            color: var(--accent);
            border-radius: var(--radius-md);
            font-size: 24px;
            margin-bottom: 20px;
        }

        .feature-card h3 {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .feature-card p {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        /* 文章内容区 */
        .article {
            display: none;
            padding: 48px 64px;
            max-width: 900px;
        }

        .article.active {
            display: block;
        }

        .article-header {
            margin-bottom: 40px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border-color);
        }

        .article-tag {
            display: inline-block;
            padding: 4px 12px;
            background: var(--accent-light);
            color: var(--accent);
            font-size: 12px;
            font-weight: 600;
            border-radius: 20px;
            margin-bottom: 16px;
        }

        .article h1 {
            font-size: 36px;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 16px;
        }

        .article-meta {
            display: flex;
            align-items: center;
            gap: 16px;
            color: var(--text-muted);
            font-size: 14px;
        }

        .article-content {
            font-size: 16px;
            line-height: 2;
            color: var(--text-primary);
        }

        .article-content p {
            margin-bottom: 20px;
        }

        .article-content h2 {
            font-size: 24px;
            font-weight: 600;
            margin: 48px 0 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
            scroll-margin-top: 100px;
        }

        .article-content h3 {
            font-size: 18px;
            font-weight: 600;
            margin: 32px 0 16px;
            scroll-margin-top: 100px;
        }

        /* 代码块样式 */
        .code-block {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 16px 20px;
            margin: 20px 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            overflow-x: auto;
        }

        /* 提示框 */
        .tip-box {
            padding: 16px 20px;
            border-radius: var(--radius-md);
            margin: 20px 0;
            display: flex;
            gap: 12px;
        }

        .tip-box.success {
            background: #f0fdf4;
            border: 1px solid #86efac;
            color: #166534;
        }

        .tip-box.warning {
            background: #fef3c7;
            border: 1px solid #fcd34d;
            color: #92400e;
        }

        [data-theme="dark"] .tip-box.success {
            background: #052e16;
            border-color: #166534;
            color: #86efac;
        }

        [data-theme="dark"] .tip-box.warning {
            background: #451a03;
            border-color: #92400e;
            color: #fcd34d;
        }

        /* 右侧目录 TOC */
        .toc {
            position: fixed;
            top: var(--header-height);
            right: 0;
            width: var(--toc-width);
            height: calc(100vh - var(--header-height));
            padding: 32px 24px;
            border-left: 1px solid var(--border-color);
            overflow-y: auto;
            display: none;
        }

        .toc.active {
            display: block;
        }

        .toc-title {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-bottom: 16px;
        }

        .toc-list {
            list-style: none;
        }

        .toc-item {
            margin-bottom: 8px;
        }

        .toc-link {
            display: block;
            font-size: 13px;
            color: var(--text-muted);
            text-decoration: none;
            padding: 4px 0;
            padding-left: 12px;
            border-left: 2px solid transparent;
            transition: var(--transition);
        }

        .toc-link:hover,
        .toc-link.active {
            color: var(--accent);
            border-left-color: var(--accent);
        }

        /* 阅读进度条 */
        .progress-bar {
            position: fixed;
            top: var(--header-height);
            left: 0;
            right: 0;
            height: 3px;
            background: var(--border-color);
            z-index: 99;
        }

        .progress-bar-fill {
            height: 100%;
            background: var(--accent);
            width: 0%;
            transition: width 0.1s ease;
        }

        /* 搜索模态框 */
        .search-modal {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.5);
            z-index: 200;
            align-items: flex-start;
            justify-content: center;
            padding-top: 100px;
        }

        .search-modal.active {
            display: flex;
        }

        .search-box {
            width: 100%;
            max-width: 600px;
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            overflow: hidden;
        }

        .search-input-wrapper {
            display: flex;
            align-items: center;
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-color);
        }

        .search-input-wrapper i {
            font-size: 20px;
            color: var(--text-muted);
            margin-right: 12px;
        }

        .search-input {
            flex: 1;
            border: none;
            background: transparent;
            font-size: 16px;
            color: var(--text-primary);
            outline: none;
            font-family: inherit;
        }

        .search-results {
            max-height: 400px;
            overflow-y: auto;
        }

        .search-result-item {
            padding: 16px 20px;
            cursor: pointer;
            transition: var(--transition);
            border-bottom: 1px solid var(--border-color);
        }

        .search-result-item:hover {
            background: var(--bg-secondary);
        }

        .search-result-item h4 {
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .search-result-item p {
            font-size: 13px;
            color: var(--text-muted);
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .search-result-item mark {
            background: var(--accent-light);
            color: var(--accent);
            padding: 0 2px;
            border-radius: 2px;
        }

        .search-empty {
            padding: 40px 20px;
            text-align: center;
            color: var(--text-muted);
        }

        /* 响应式 */
        @media (max-width: 1200px) {
            .toc {
                display: none !important;
            }
            .main {
                margin-right: 0;
            }
        }

        @media (max-width: 900px) {
            .sidebar {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }
            .sidebar.open {
                transform: translateX(0);
            }
            .main {
                margin-left: 0;
            }
            .hero h1 {
                font-size: 32px;
            }
            .features {
                grid-template-columns: 1fr;
                padding: 32px 24px;
            }
            .article {
                padding: 32px 24px;
            }
            .header-nav {
                display: none;
            }
        }

        /* 滚动条 */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }

        /* 移动端菜单按钮 */
        .menu-toggle {
            display: none;
            width: 40px;
            height: 40px;
            align-items: center;
            justify-content: center;
            border: none;
            background: transparent;
            color: var(--text-primary);
            cursor: pointer;
            font-size: 24px;
        }

        @media (max-width: 900px) {
            .menu-toggle {
                display: flex;
            }
        }
    </style>
</head>
<body>
    <!-- 阅读进度条 -->
    <div class="progress-bar">
        <div class="progress-bar-fill" id="progressBar"></div>
    </div>

    <!-- 顶部导航 -->
    <header class="header">
        <div class="header-left">
            <button class="menu-toggle" id="menuToggle">
                <i class="ri-menu-line"></i>
            </button>
            <a href="#" class="logo" onclick="showHome(); return false;">
                <i class="ri-brain-line"></i>
                <span>EZLLM</span>
            </a>
            <nav class="header-nav">
                <a href="#" class="active" onclick="showHome(); return false;">首页</a>
                <a href="#" onclick="loadDocument(0); return false;">文档</a>
            </nav>
        </div>
        <div class="header-right">
            <div class="search-trigger" id="searchTrigger">
                <i class="ri-search-line"></i>
                <span>搜索文档...</span>
                <kbd>Ctrl K</kbd>
            </div>
            <button class="theme-toggle" id="themeToggle" title="切换主题">
                <i class="ri-sun-line"></i>
            </button>
        </div>
    </header>

    <div class="container">
        <!-- 侧边栏 -->
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-section">
                <div class="sidebar-title">学习文档</div>
                <ul class="nav-list" id="navList">
                    <!-- 动态生成 -->
                </ul>
            </div>
        </aside>

        <!-- 主内容 -->
        <main class="main" id="mainContent">
            <!-- 首页 Hero -->
            <section class="hero" id="heroSection">
                <div class="hero-badge">
                    <i class="ri-sparkle-line"></i>
                    开源 · 免费 · 持续更新
                </div>
                <h1>EZLLM</h1>
                <p>零基础学大模型<br>从入门到精通，用最通俗的语言讲解 AI</p>
                <div class="hero-buttons">
                    <button class="btn btn-primary" onclick="loadDocument(0)">
                        <i class="ri-book-open-line"></i>
                        开始学习
                    </button>
                    <a class="btn btn-secondary" href="https://github.com" target="_blank">
                        <i class="ri-github-line"></i>
                        GitHub
                    </a>
                </div>
            </section>

            <!-- 特性卡片 -->
            <section class="features" id="featuresSection">
                <!-- 动态生成 -->
            </section>

            <!-- 文章内容区 -->
            <article class="article" id="articleSection">
                <div class="article-header">
                    <span class="article-tag" id="articleTag">文档</span>
                    <h1 id="articleTitle">标题</h1>
                    <div class="article-meta">
                        <span><i class="ri-time-line"></i> 阅读约 5 分钟</span>
                    </div>
                </div>
                <div class="article-content" id="articleContent">
                    <!-- 文章内容 -->
                </div>
            </article>
        </main>

        <!-- 右侧目录 -->
        <aside class="toc" id="tocSection">
            <div class="toc-title">本文目录</div>
            <ul class="toc-list" id="tocList">
                <!-- 动态生成 -->
            </ul>
        </aside>
    </div>

    <!-- 搜索模态框 -->
    <div class="search-modal" id="searchModal">
        <div class="search-box">
            <div class="search-input-wrapper">
                <i class="ri-search-line"></i>
                <input type="text" class="search-input" id="searchInput" placeholder="输入关键词搜索...">
            </div>
            <div class="search-results" id="searchResults">
                <div class="search-empty">输入关键词开始搜索</div>
            </div>
        </div>
    </div>

    <script>
        // 文档数据
        const documents = __DATA_PLACEHOLDER__;

        // DOM 元素
        const navList = document.getElementById('navList');
        const heroSection = document.getElementById('heroSection');
        const featuresSection = document.getElementById('featuresSection');
        const articleSection = document.getElementById('articleSection');
        const articleTitle = document.getElementById('articleTitle');
        const articleContent = document.getElementById('articleContent');
        const articleTag = document.getElementById('articleTag');
        const tocSection = document.getElementById('tocSection');
        const tocList = document.getElementById('tocList');
        const progressBar = document.getElementById('progressBar');
        const searchModal = document.getElementById('searchModal');
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        const themeToggle = document.getElementById('themeToggle');
        const sidebar = document.getElementById('sidebar');
        const menuToggle = document.getElementById('menuToggle');

        let currentDocIndex = -1;

        // 初始化
        function init() {
            renderNavigation();
            renderFeatures();
            initTheme();
            initSearch();
            initScrollProgress();
            initMobileMenu();
        }

        // 渲染导航
        function renderNavigation() {
            navList.innerHTML = '';
            documents.forEach((doc, index) => {
                const li = document.createElement('li');
                li.className = 'nav-item';
                li.innerHTML = `
                    <a class="nav-link" data-index="${index}" onclick="loadDocument(${index})">
                        <i class="ri-file-text-line"></i>
                        <span>${doc.title}</span>
                    </a>
                `;
                navList.appendChild(li);
            });
        }

        // 渲染特性卡片
        function renderFeatures() {
            const icons = ['ri-brain-line', 'ri-eye-line', 'ri-magic-line', 'ri-code-line', 'ri-lightbulb-line', 'ri-rocket-line'];
            featuresSection.innerHTML = '';
            documents.slice(0, 6).forEach((doc, index) => {
                const card = document.createElement('div');
                card.className = 'feature-card';
                card.onclick = () => loadDocument(index);

                const title = doc.title.replace(/^\\d+\\./, '').trim();
                const preview = doc.content.substring(0, 80) + '...';

                card.innerHTML = `
                    <div class="feature-icon">
                        <i class="${icons[index % icons.length]}"></i>
                    </div>
                    <h3>${title}</h3>
                    <p>${preview}</p>
                `;
                featuresSection.appendChild(card);
            });
        }

        // 显示首页
        function showHome() {
            heroSection.style.display = 'block';
            featuresSection.style.display = 'grid';
            articleSection.classList.remove('active');
            tocSection.classList.remove('active');
            currentDocIndex = -1;

            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });

            // 更新导航状态
            document.querySelectorAll('.header-nav a').forEach((a, i) => {
                a.classList.toggle('active', i === 0);
            });
        }

        // 加载文档
        function loadDocument(index) {
            const doc = documents[index];
            if (!doc) return;

            currentDocIndex = index;

            // 隐藏首页，显示文章
            heroSection.style.display = 'none';
            featuresSection.style.display = 'none';
            articleSection.classList.add('active');
            tocSection.classList.add('active');

            // 设置内容
            const title = doc.title.replace(/^\\d+\\./, '').trim();
            articleTitle.textContent = title;
            articleTag.textContent = '第 ' + (index + 1) + ' 章';

            // 解析内容，将段落转换为 HTML
            const content = parseContent(doc.content);
            articleContent.innerHTML = content;

            // 生成目录
            renderTOC(doc.headings || []);

            // 更新导航高亮
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.toggle('active', parseInt(link.dataset.index) === index);
            });

            // 更新顶部导航
            document.querySelectorAll('.header-nav a').forEach((a, i) => {
                a.classList.toggle('active', i === 1);
            });

            // 滚动到顶部
            window.scrollTo({ top: 0, behavior: 'smooth' });

            // 关闭移动端菜单
            sidebar.classList.remove('open');
        }

        // 解析内容
        function parseContent(text) {
            const lines = text.split('\\n');
            let html = '';
            let inParagraph = false;

            lines.forEach(line => {
                line = line.trim();
                if (!line) {
                    if (inParagraph) {
                        html += '</p>';
                        inParagraph = false;
                    }
                    return;
                }

                // 检测标题（以？结尾的短句）
                if ((line.endsWith('？') || line.endsWith('?')) && line.length < 30) {
                    if (inParagraph) {
                        html += '</p>';
                        inParagraph = false;
                    }
                    const id = 'heading-' + line.replace(/[^\\w\\u4e00-\\u9fa5]/g, '').substring(0, 10);
                    html += `<h2 id="${id}">${line}</h2>`;
                    return;
                }

                // 检测提示框
                if (line.startsWith('❌')) {
                    if (inParagraph) { html += '</p>'; inParagraph = false; }
                    html += `<div class="tip-box warning"><i class="ri-close-circle-line"></i><div>${line}</div></div>`;
                    return;
                }
                if (line.startsWith('✅')) {
                    if (inParagraph) { html += '</p>'; inParagraph = false; }
                    html += `<div class="tip-box success"><i class="ri-checkbox-circle-line"></i><div>${line}</div></div>`;
                    return;
                }

                // 普通段落
                if (!inParagraph) {
                    html += '<p>';
                    inParagraph = true;
                } else {
                    html += '<br>';
                }
                html += line;
            });

            if (inParagraph) {
                html += '</p>';
            }

            return html;
        }

        // 渲染目录
        function renderTOC(headings) {
            tocList.innerHTML = '';
            if (headings.length === 0) {
                tocSection.classList.remove('active');
                return;
            }
            headings.forEach(heading => {
                const li = document.createElement('li');
                li.className = 'toc-item';
                const id = 'heading-' + heading.replace(/[^\\w\\u4e00-\\u9fa5]/g, '').substring(0, 10);
                li.innerHTML = `<a class="toc-link" href="#${id}">${heading}</a>`;
                tocList.appendChild(li);
            });
        }

        // 主题切换
        function initTheme() {
            const savedTheme = localStorage.getItem('theme');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

            if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
                document.body.dataset.theme = 'dark';
                themeToggle.innerHTML = '<i class="ri-moon-line"></i>';
            }

            themeToggle.addEventListener('click', () => {
                const isDark = document.body.dataset.theme === 'dark';
                document.body.dataset.theme = isDark ? '' : 'dark';
                themeToggle.innerHTML = isDark ? '<i class="ri-sun-line"></i>' : '<i class="ri-moon-line"></i>';
                localStorage.setItem('theme', isDark ? 'light' : 'dark');
            });
        }

        // 搜索功能
        function initSearch() {
            const searchTrigger = document.getElementById('searchTrigger');

            searchTrigger.addEventListener('click', () => {
                searchModal.classList.add('active');
                searchInput.focus();
            });

            searchModal.addEventListener('click', (e) => {
                if (e.target === searchModal) {
                    searchModal.classList.remove('active');
                    searchInput.value = '';
                    searchResults.innerHTML = '<div class="search-empty">输入关键词开始搜索</div>';
                }
            });

            // Ctrl+K 快捷键
            document.addEventListener('keydown', (e) => {
                if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                    e.preventDefault();
                    searchModal.classList.add('active');
                    searchInput.focus();
                }
                if (e.key === 'Escape') {
                    searchModal.classList.remove('active');
                }
            });

            searchInput.addEventListener('input', (e) => {
                const keyword = e.target.value.toLowerCase().trim();
                if (!keyword) {
                    searchResults.innerHTML = '<div class="search-empty">输入关键词开始搜索</div>';
                    return;
                }

                const results = documents.filter(doc =>
                    doc.title.toLowerCase().includes(keyword) ||
                    doc.content.toLowerCase().includes(keyword)
                );

                if (results.length === 0) {
                    searchResults.innerHTML = '<div class="search-empty">未找到相关文档</div>';
                    return;
                }

                searchResults.innerHTML = results.map(doc => {
                    const index = documents.indexOf(doc);
                    const title = doc.title.replace(new RegExp(keyword, 'gi'), '<mark>$&</mark>');
                    let preview = doc.content.substring(0, 100);
                    preview = preview.replace(new RegExp(keyword, 'gi'), '<mark>$&</mark>');

                    return `
                        <div class="search-result-item" onclick="loadDocument(${index}); searchModal.classList.remove('active');">
                            <h4>${title}</h4>
                            <p>${preview}...</p>
                        </div>
                    `;
                }).join('');
            });
        }

        // 阅读进度
        function initScrollProgress() {
            window.addEventListener('scroll', () => {
                const scrollTop = window.scrollY;
                const docHeight = document.documentElement.scrollHeight - window.innerHeight;
                const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
                progressBar.style.width = progress + '%';
            });
        }

        // 移动端菜单
        function initMobileMenu() {
            menuToggle.addEventListener('click', () => {
                sidebar.classList.toggle('open');
            });
        }

        // 启动
        init();
    </script>
</body>
</html>
'''

    # 替换数据占位符
    html_content = html_template.replace("__DATA_PLACEHOLDER__", js_data)

    # 输出文件
    output_path = os.path.join(base_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] Success! Generated website with {len(documents)} documents")
    print(f"[FILE] Output: {output_path}")
    print(f"[TIP] Open index.html to preview, or push to GitHub Pages")

if __name__ == "__main__":
    build_site()
