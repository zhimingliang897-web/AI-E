# 📥 免费剪贴画自动下载器

> 专注于**免费素材剪贴画（clipart）**的自动下载工具  
> 自动从JSON中筛选`type='clipart'`，忽略AI视频和AI图片

## 🎯 核心功能

**脚本做什么：**
1. ✅ 读取你的完整 `script_needs.json`（可以混合多种type）
2. ✅ 自动筛选其中 `type='clipart'` 的条目
3. ✅ 对每个clipart生成搜索关键词
4. ✅ 从4个免费图库搜索下载：unDraw、Storyset、Wikimedia、OpenMoji
5. ✅ 保存到 `assets/manual/` 目录

**脚本自动忽略：**
- ⚠️ `ai_video` 类型（不处理）
- ⚠️ `ai_image` 类型（不处理）
- ⚠️ 其他任何非clipart的type

---

## 📂 文件结构

```
scripts/
├── clipart_downloader_v2.py                 # 主脚本（改进版）⭐
├── starter.py                               # 交互式启动器
│
├── CLIPART_DOWNLOADER_QUICK_REFERENCE.md   # 快速参考卡 ⭐⭐
├── CLIPART_DOWNLOADER_GUIDE.md             # 完整使用指南
├── IMPROVEMENTS_ANALYSIS.md                # 改进分析对比
│
├── example_clipart_needs.json               # 示例配置文件
└── README.md                                # 本文件

projects/
├── day2/
│   └── script_needs.json                    # 实际项目需求文件
├── day3/
│   └── script_needs.json
└── ...

assets/
└── manual/                                  # 下载的素材保存位置
    ├── 15_image_to_text_illustration.png
    ├── 15_image_to_text_icon.png
    └── ...
```

---

## 🚀 快速开始（3步）

### 1️⃣ 安装依赖
```bash
pip install requests
```

### 2️⃣ 准备JSON（包含完整的needs_list）
```json
{
  "needs_list": [
    {
      "scene_id": "01_ai_intro",
      "type": "clipart",
      "description": "robot artificial intelligence",
      "is_optional": false
    },
    {
      "scene_id": "02_ml_learning",
      "type": "clipart",
      "description": "machine learning algorithm",
      "is_optional": false
    }
    // ⚠️ 可以添加ai_video和ai_image，脚本会自动忽略它们
  ]
}
```

### 3️⃣ 运行脚本
```bash
# 预览（推荐先用）
python scripts/clipart_downloader_v2.py projects/day2/script_needs.json --dry-run

# 下载
python scripts/clipart_downloader_v2.py projects/day2/script_needs.json
```

---

## ⚡ 工作流

```
你提供完整的JSON (包含多种type)
            ↓
脚本读取needs_list
            ↓
自动筛选 type='clipart' ✅
自动忽略 ai_video, ai_image ⚠️
            ↓
生成关键词 → 搜索 → 下载
            ↓
保存到 assets/manual/
```

### 输出文件示例

```
assets/manual/
├── 01_ai_intro_illustration.png    # clipart 插画
├── 01_ai_intro_icon.png            # clipart 图标
├── 02_ml_learning_illustration.png
├── 02_ml_learning_icon.png
└── ...
```

---

## 📚 文档导航

| 文档 | 用途 | 对象 |
|------|------|------|
| **[CLIPART_DOWNLOADER_QUICK_REFERENCE.md](CLIPART_DOWNLOADER_QUICK_REFERENCE.md)** | 常用命令速查表 | 所有用户 |
| **[CLIPART_DOWNLOADER_GUIDE.md](CLIPART_DOWNLOADER_GUIDE.md)** | 完整使用指南 | 需要详细说明的用户 |
| **[IMPROVEMENTS_ANALYSIS.md](IMPROVEMENTS_ANALYSIS.md)** | v1.0 → v2.0改进详解 | 对代码感兴趣的用户 |

### 我应该看哪个文档？

- 👀 **刚开始，想了解基本用法？** → 看[快速参考卡](CLIPART_DOWNLOADER_QUICK_REFERENCE.md)
- 🔍 **想深入了解每个功能？** → 看[完整使用指南](CLIPART_DOWNLOADER_GUIDE.md)
- 🛠️ **想了解代码是如何改进的？** → 看[改进分析](IMPROVEMENTS_ANALYSIS.md)
- 🤔 **遇到问题，想找解决方案？** → [快速参考卡的故障排查章节](CLIPART_DOWNLOADER_QUICK_REFERENCE.md#故障排查快速方案)

---

## 🎨 支持的图库

| 图库 | 特色 | 授权 |
|------|------|------|
| **unDraw** | 现代扁平风设计插画 | MIT |
| **Storyset** | 色彩丰富的场景插画 | 免费 |
| **Wikimedia Commons** | 高质量多样化图片 | CC多种 |
| **OpenMoji** | 开源emoji表情 | CC BY-SA 4.0 |

脚本会自动轮询所有图库，智能选择可用的源。

---

## 💡 完整工作流示例

### 场景：提供完整JSON，自动筛选clipart下载

```bash
# 1. 准备完整的needs.json（包含all type）
cat > projects/day2/script_needs.json << 'EOF'
{
  "needs_list": [
    {
      "scene_id": "01_ai_intro",
      "type": "clipart",
      "description": "robot data technology"
    },
    {
      "scene_id": "02_ml_concept", 
      "type": "clipart",
      "description": "machine learning algorithm"
    },
    {
      "scene_id": "03_avatar",
      "type": "ai_video",  // 脚本会自动忽略这个
      "prompt": "3D avatar"
    }
  ]
}
EOF

# 2. 预览要处理的clipart任务
python scripts/clipart_downloader_v2.py projects/day2/script_needs.json --dry-run
# 输出：只显示 01_ai_intro 和 02_ml_concept
#      自动跳过 03_avatar (ai_video type)

# 3. 开始下载clipart
python scripts/clipart_downloader_v2.py projects/day2/script_needs.json

# 4. 检查结果
ls assets/manual/
# 应该看到：
# - 01_ai_intro_illustration.png
# - 01_ai_intro_icon.png
# - 02_ml_concept_illustration.png
# - 02_ml_concept_icon.png
```

**脚本的好处：** 你可以在JSON中放所有类型的需求，脚本会自动聪明地只处理clipart！

---

## 🔧 主要特性

### ✨ 智能筛选
- ✅ 自动从完整JSON中筛选clipart
- ✅ 自动忽略ai_video、ai_image等
- ✅ 一次提供，自动处理，无需手动提取

### 📥 高效下载
- ✅ 支持4个免费图库（unDraw、Storyset、Wikimedia、OpenMoji）
- ✅ 多库轮询，自动选择最优源
- ✅ 每个clipart下载2个文件：插画 + 图标

### ⚡ 聪明缓存
- ✅ 本地文件自动检查
- ✅ 已有文件直接跳过
- ✅ 损坏文件自动重新下载

---

## ⚡ 性能指标

| 指标 | 数值 |
|------|------|
| 支持图库数 | 4个 |
| 平均下载时间/个 | 2-5秒（取决于网络） |
| 本地文件检查 | <1ms |
| 关键词生成 | <1ms |
| 日志文件大小 | ~50-100KB |

---

## 🐛 已知限制和解决方案

| 限制 | 原因 | 解决方案 |
|------|------|---------|
| 某些图库可能无法访问 | GFW/网络问题 | 使用VPN或代理 |
| 某些关键词找不到图片 | 图库中确实没有 | 修改description，用更通用的词 |
| 下载速度慢 | 访问国外服务器 | 使用代理，或分批下载 |
| 图片不符合预期 | 关键词有歧义 | 手动修改description重试 |

---

## 🎓 学习路径

### 如果你是初学者：
1. 阅读[快速参考卡](CLIPART_DOWNLOADER_QUICK_REFERENCE.md)的"最常用命令"和"工作流整体步骤"
2. 用`--dry-run`模式测试
3. 实际执行下载
4. 查看logs文件理解过程

### 如果你想深入学习：
1. 阅读[完整使用指南](CLIPART_DOWNLOADER_GUIDE.md)了解每个功能
2. 查看[改进分析](IMPROVEMENTS_ANALYSIS.md)理解代码设计
3. 阅读脚本源代码中的详细注释
4. 尝试修改脚本或添加新图库

### 如果你想扩展功能：
1. 研究`LibraryDownloader`基类的设计
2. 创建新的Downloader子类（参考unDraw的实现）
3. 在`download_clipart_asset`函数中注册新下载器
4. 参考[改进分析](IMPROVEMENTS_ANALYSIS.md)中的模块化说明

---

## ❓ FAQ

**Q: 脚本可以运行在哪些操作系统？**
A: Window、Linux、macOS都支持（Python 3.7+）

**Q: 下载的图片格式是什么？**
A: 主要是PNG，部分可能是SVG或其他格式。都保存为`.png`扩展名

**Q: 可以批量修改已下载的文件名吗？**
A: 可以，只需保持格式 `{scene_id}_{type}.png`（illustration或icon）

**Q: 如何添加新的图库支持？**
A: 参考[改进分析](IMPROVEMENTS_ANALYSIS.md)中的"模块化"部分，创建新的Downloader类

**Q: 脚本会删除什么文件吗？**
A: 只会删除<1KB的损坏文件（重新下载）。其他情况不会删除

**Q: 如何离线使用？**
A: 使用`--dry-run`模式预览，然后手动下载图片保存到`assets/manual/`

---

## 📞 获取帮助

### 遇到问题时：

1. **检查日志文件**
   ```bash
   tail -100 asset_download.log
   ```

2. **查看故障排查指南**
   - [快速参考卡 - 故障排查章节](CLIPART_DOWNLOADER_QUICK_REFERENCE.md#故障排查快速方案)
   - [使用指南 - 常见问题章节](CLIPART_DOWNLOADER_GUIDE.md#常见问题)

3. **检查环境**
   ```bash
   python scripts/starter.py --check
   ```

4. **使用DRY-RUN验证配置**
   ```bash
   python scripts/clipart_downloader_v2.py your_config.json --dry-run
   ```

---

## 📊 版本历史

### v2.0 (当前) - 生产级版本
- ✨ 完全重写，模块化架构
- ✨ 支持4个免费图库
- ✨ 添加DRY-RUN预览模式
- ✨ 本地文件检查，避免重复下载
- ✨ 完整的文档和示例
- 📈 代码质量显著提升
- 🐛 修复多个v1.0中的bug
- 📚 提供详尽的使用指南和快速参考

### v1.0 - 初版本
- 基础的下载功能
- 支持unDraw和Wikimedia
- 从stdin读取JSON

---

## 🙏 致谢

感谢以下开源项目和免费资源库的支持：

- **unDraw** - MIT License, 现代设计插画
- **Storyset** - 免费可商用插画
- **Wikimedia Commons** - 开放知识库
- **OpenMoji** - CC BY-SA 4.0, 开源表情库

---

## 📄 许可证

本脚本采用 **MIT License**，可自由使用、修改和分发。

---

## 🔄 更新和反馈

有问题或建议？

- 检查日志文件了解详细信息
- 查看相关文档获取解决方案
- 修改脚本并测试自定义配置

---

**祝使用愉快！** 🎉

👨‍💻 **快速开始：**
```bash
# 1. 安装依赖
pip install requests

# 2. 预览任务
python scripts/clipart_downloader_v2.py projects/day2/script_needs.json --dry-run

# 3. 开始下载
python scripts/clipart_downloader_v2.py projects/day2/script_needs.json
```

---

**最后更新**: 2026-02-24  
**脚本版本**: v2.0  
**文档完整性**: ⭐⭐⭐⭐⭐
