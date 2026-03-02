# AutoVideo 命令快速指南

本文档提供 v3.0 版本的常用命令示例，按使用场景分类。

---

## 一、工作流概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        Plan 阶段                                 │
│  草稿文案 + Avatar视频 → LLM导演 → script.json + needs_list     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     素材准备阶段                                 │
│  根据 needs_list 准备素材（AI生图/免费图库/用户自备）            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       Build 阶段                                 │
│  script.json + 素材 + TTS → 最终视频 + SRT字幕                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、Plan 阶段命令

### 基础模式（图片 + edge-tts）

```bash
# 最简用法：草稿文案 + Avatar
python pipeline.py plan \
  --project projects/MyVideo \
  --text draft.txt \
  --avatar input/my_avatar.mp4
```

### 导演风格预设

```bash
# 标准导演（默认）
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4

# 概念科普导演（偏好 manim + split_screen）
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --director concept

# 激情叙事导演（快切 + 全屏画面）
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --director narrative

# 电影感导演（搭配 --mode video 效果最佳）
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --director cinematic
```

### AI 视频模式

```bash
# 启用 ai_video 类型（每视频最多 2 个动态镜头）
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --mode video

# 推荐组合：AI视频 + 电影感导演
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --mode video --director cinematic
```

### 多语言支持

```bash
# 自动检测语言（默认）
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --lang auto

# 强制中文输出
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --lang zh

# 强制英文输出
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --lang en
```

---

## 三、带标注文案转换（v3.0 新增）

使用独立的标注转换器，支持在 txt 中标注自备素材和特效：

### 标注语法

```
[xxx.png]           → 用户自备图片
[xxx.mp4]           → 用户自备视频
{特效：描述}         → 特效标注
【画面】...【/画面】 → 画面描述（不朗读）
【配音】...         → 配音文本（TTS朗读）
```

### 转换命令

```bash
# 基础用法
python -m parser.annotated_converter my_script.txt -o script.json --avatar

# 指定输出路径
python -m parser.annotated_converter my_script.txt -o projects/MyVideo/script.json --avatar

# 指定配置文件
python -m parser.annotated_converter my_script.txt -o script.json --avatar --config projects/MyVideo/config.yaml
```

### 示例文案

```
=== 第一幕：什么是生成式模型？ ===

【画面】
屏幕左边出现分类机 [cat_dog.jpg] {特效：头上闪烁公式}
右边出现魔法画笔 {特效：光效闪烁}，画出 [cyber_cat.png]
【/画面】

【配音】
大家都在聊大模型，这背后的核心主角，叫"生成式模型"。
```

---

## 四、Build 阶段命令

### 基础构建

```bash
# 使用项目目录（推荐）
python pipeline.py build --project projects/MyVideo

# 使用指定脚本文件
python pipeline.py build --script path/to/script.json
```

### 分步构建

```bash
# 仅运行 Avatar 切割
python pipeline.py build --project projects/MyVideo --only avatar

# 仅运行 TTS 配音
python pipeline.py build --project projects/MyVideo --only tts

# 仅运行 AI 生图
python pipeline.py build --project projects/MyVideo --only images
```

### 多语言构建

```bash
# 构建中文版本
python pipeline.py build --project projects/MyVideo --lang zh

# 构建英文版本
python pipeline.py build --project projects/MyVideo --lang en
```

---

## 五、TTS 语音配置

### edge-tts（默认，免费云端）

```yaml
# config.yaml
tts:
  enabled: true
  provider: "edge"
  padding_duration: 0.3         # 句间停顿秒数
  voice: "zh-CN-YunxiNeural"    # 推荐男声
  rate: "-8%"                   # 稍慢语速
  pitch: "+0Hz"
```

常用中文声音：
- `zh-CN-YunxiNeural` - 男声，小说/故事风，最自然
- `zh-CN-YunyangNeural` - 男声，新闻播报风，沉稳
- `zh-CN-XiaoxiaoNeural` - 女声，新闻/小说风
- `zh-CN-XiaoyiNeural` - 女声，卡通风，活泼轻快
- `zh-TW-HsiaoChenNeural` - 女声，台湾腔
- `zh-HK-HiuMaanNeural` - 女声，粤语

常用英文声音：
- `en-US-JennyNeural` - 美式女声，自然亲切
- `en-US-ChristopherNeural` - 美式男声，低沉纪录片旁白
- `en-GB-SoniaNeural` - 英式女声，优雅伦敦音

### ChatTTS（v3.0 新增，本地模型）

```yaml
# config.yaml
tts:
  enabled: true
  provider: "chattts"
  padding_duration: 0.3   # 句间停顿秒数
  seed: 2222              # 音色种子（换数字换声音）
  speed: 5                # 语速 1-9
  oral: 3                 # 口语化 0-9
  laugh: 1                # 笑声 0-2
  break_: 5               # 停顿 0-7
```

### 声音试听工具

```bash
# 交互式试听 edge-tts 和 ChatTTS 的各种声音
python tools/voice_test.py
```

---

## 六、素材准备

### 自动下载免费素材

```bash
# 根据 needs_list 从 Pixabay 下载素材
python scripts/auto_fetch_assets.py --project projects/MyVideo

# 跳过已存在的素材
python scripts/auto_fetch_assets.py --project projects/MyVideo --skip-existing
```

### 手动准备素材

```bash
# 素材放置路径
projects/MyVideo/assets/
├── images/         # AI 生图 / 手动图片（{scene_id}.png）
├── videos/         # AI 视频 / 手动视频（{scene_id}.mp4）
├── manual/         # 用户标注的自备素材
├── audio/          # TTS 生成的语音
└── avatar/         # Avatar 切割后的片段
```

---

## 七、项目清理

```bash
# 安全清理（debug 文件、缓存）
python cleanup_project.py --project MyVideo

# 深度清理（包括输出文件）
python cleanup_project.py --project MyVideo --deep

# 预览清理内容
python cleanup_project.py --project MyVideo --dry-run
```

---

## 八、完整工作流示例

### 示例 1：标准科普视频

```bash
# 1. Plan：生成脚本
python pipeline.py plan \
  --project projects/ai_intro \
  --text ai_intro.txt \
  --avatar input/presenter.mp4

# 2. 下载素材
python scripts/auto_fetch_assets.py --project projects/ai_intro

# 3. Build：合成视频
python pipeline.py build --project projects/ai_intro
```

### 示例 2：电影感 AI 视频

```bash
# 1. Plan：启用 AI 视频 + 电影导演
python pipeline.py plan \
  --project projects/movie_style \
  --text script.txt \
  --avatar input/avatar.mp4 \
  --mode video \
  --director cinematic

# 2. 根据 needs_list 生成 AI 视频
# 使用 Runway/Pika/可灵 等工具生成，放入 assets/videos/

# 3. Build
python pipeline.py build --project projects/movie_style
```

### 示例 3：带标注的创意视频（v3.0）

```bash
# 1. 准备带标注的文案 creative.txt
# 包含 [my_image.png] {特效：xxx} 等标注

# 2. 使用标注转换器
python -m parser.annotated_converter creative.txt \
  -o projects/creative/script.json \
  --avatar

# 3. 准备标注的素材
# 将 my_image.png 等放入 projects/creative/assets/manual/

# 4. Build
python pipeline.py build --project projects/creative
```

### 示例 4：使用 ChatTTS 本地语音

```bash
# 1. 修改 config.yaml
# tts.provider: "chattts"
# tts.seed: 2222

# 2. 试听不同音色
python tools/voice_test.py

# 3. 正常 Plan + Build
python pipeline.py plan --project projects/my_video --text draft.txt --avatar input/avatar.mp4
python pipeline.py build --project projects/my_video
```

---

## 九、参数速查表

### plan 命令

| 参数 | 说明 | 示例 |
|------|------|------|
| `--project` | 项目目录 | `projects/MyVideo` |
| `--text` | 草稿文案路径 | `draft.txt` |
| `--avatar` | Avatar 视频路径 | `input/avatar.mp4` |
| `--mode` | 素材模式 | `image`（默认） / `video` |
| `--director` | 导演风格 | `standard` / `concept` / `narrative` / `cinematic` |
| `--lang` | 输出语言 | `auto` / `zh` / `en` |
| `--output` | 脚本输出路径 | `path/to/script.json` |

### build 命令

| 参数 | 说明 | 示例 |
|------|------|------|
| `--project` | 项目目录 | `projects/MyVideo` |
| `--script` | 脚本文件路径 | `path/to/script.json` |
| `--lang` | 读取语言变体 | `zh` / `en` |
| `--only` | 仅执行某步骤 | `avatar` / `tts` / `images` |

### annotated_converter 命令

| 参数 | 说明 | 示例 |
|------|------|------|
| `input` | 输入文案路径 | `my_script.txt` |
| `-o` | 输出 JSON 路径 | `script.json` |
| `--avatar` | 启用 Avatar 模式 | （无值，开关） |
| `--config` | 配置文件路径 | `config.yaml` |
| `--lang` | 输出语言 | `zh` / `en` |

---

## 十、常见问题

### Q: ChatTTS 报错 transformers 版本冲突？
A: 已通过子进程隔离解决，确保 `CHATTTS_PATH` 配置正确即可。

### Q: 用户标注的素材没有被保留？
A: 使用 `parser/annotated_converter.py` 而不是 `script_converter.py`。

### Q: 如何调整 ChatTTS 音色？
A: 修改 `config.yaml` 中的 `tts.seed`，或使用 `python tools/voice_test.py` 试听。

### Q: AI 视频生成后放哪里？
A: 放入 `projects/MyVideo/assets/videos/{scene_id}.mp4`，文件名与 needs_list 中的 scene_id 对应。

---

更多详细文档：
- [README.md](README.md) - 完整功能说明
- [CHANGELOG.md](CHANGELOG.md) - 版本变更记录
- [parser/ANNOTATION_GUIDE.md](parser/ANNOTATION_GUIDE.md) - 标注格式详解
