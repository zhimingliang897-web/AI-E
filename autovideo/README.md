# AutoVideo - 智能视频生产 Pipeline

## 快速上手：推荐单项目工作流（示例 day4）

```bash
# 1) 用导演模式生成脚本（plan）
python pipeline.py plan --project projects/day4 --text day4.txt --avatar input/aiernewA--hanxiuyun.mp4 --mode video --director cinematic

# 2) 根据 script_needs.json 自动下载剪贴画素材到 assets/manual
python scripts/clipart_downloader_v2.py projects/day4/script_needs.json --output assets/manual
# 或：
# cat projects/day4/script_needs.json | python scripts/clipart_downloader_v2.py

指定目录：
python scripts/clipart_downloader_v2.py projects/day4/script_needs.json --output projects/day4/assets/manual
# 或：
# cat projects/day4/script_needs.json | python scripts/clipart_downloader_v2.py --output projects/day4/assets/manual

# 3) 为该项目的所有 Manim 场景生成/修复代码（按项目归档到 visuals/generated_scenes/day4/）
python tools/manim_test.py projects/day4/script.json

# 4) 跑完整 build，合成 Day4 视频
python pipeline.py build --project projects/day4
#
# 5) 检查素材完整性（强烈建议）
python check_assets.py day4
```

## 素材路径问题与检查工具

如果你发现生成的视频某些场景背景是空的（只有纯色，没有图片），很可能是素材路径不匹配。

### 解决方案

```bash
python check_assets.py day4
```

### 状态说明

| 状态 | 含义 |
|------|------|
| 错误: 0, 警告: 0 | 完美，可以直接生成 |
| 错误: 0, 警告: >0 | 代码已自动修复 |
| 错误: >0 | 需要补充素材 |

`compositor/assembler.py` 已内置智能路径查找功能。

一套 Python 全栈视频自动化工具链，支持以 **最高效直观** 的方式构建项目。本文档结构按版本时间倒序排列，优先展示当前最强大的功能与模式。

## 版本脉络与模式快览


| 版本     | 模式               | 核心升级点 / 工作流                                                                                  |
| -------- | ------------------ | ---------------------------------------------------------------------------------------------------- |
| **v3.0** | 标注模式 + ChatTTS | 用户可在 txt 中标注自备素材`[xxx.png]` 和特效 `{特效：xxx}`，LLM 原样保留；新增 ChatTTS 本地语音引擎 |
| **v2.9** | 视觉润色           | Enhanced Ken Burns（pan+zoom 8方向）+ 字幕淡入 + solid_bg 主题配色 + Avatar PiP 软阴影               |
| **v2.8** | AI 视频模式        | **`--mode video`** 双轨模式 + ai_video 类型支持 + 导演 cinematic 预设 + 自动生成 ai_video 需求单     |
| **v2.7** | 导演引擎升级       | 动态导演预设模板 + Avatar 自动循环防定格 + 纯色卡片智能去重 + 免费素材精准英文索词 + 标题卡时长优化  |
| **v2.6** | 导演与转场增强     | 逐场景 transition 生效 + txt→json 规范化 + 智能限制付费 ai_image 比例的低成本策略                   |
| **v2.5** | 可读性与清理优化   | 修复 title_card 取值 + 字体视效参数全面优化 + 新增一键清理脚本                                       |
| **v2.1** | 稳定性修复         | 修复 Windows 编码/空音频/临时文件问题 + 安全字幕边距处理                                             |
| **v2**   | Avatar 导演模式    | 文案 + Avatar 素材 → LLM 智能导演 → 需求清单 → 补充素材 → 一键合成                               |
| **v1**   | 基础组装模式       | 纯文本 → LLM 切分转 JSON → TTS 配音 → AI 生图 → 简单拼接影片                                     |

---

## 最新特性 (v3.0) — 标注模式 + ChatTTS

### 用户标注保留

新增独立转换器 `parser/annotated_converter.py`，支持在 txt 文案中标注自备素材和特效，LLM 导演会**原样保留**这些标注：

**标注语法：**


| 标注类型  | 语法                   | 示例                            |
| --------- | ---------------------- | ------------------------------- |
| 图片/视频 | `[文件名.扩展名]`      | `[cyber_cat.png]`、`[demo.mp4]` |
| 特效描述  | `{特效：描述}`         | `{特效：光效闪烁}`              |
| 画面段落  | `【画面】...【/画面】` | 画面描述，不朗读                |
| 配音段落  | `【配音】...`          | 配音文本，TTS 朗读              |

**示例文案：**

```
=== 第一幕 ===

【画面】
展示赛博朋克猫 [cyber_cat.png] {特效：光效闪烁}
【/画面】

【配音】
这是一只 AI 生成的猫。
```

**运行命令：**

```bash
# 使用标注转换器
python -m parser.annotated_converter my_script.txt -o script.json --avatar

# 将素材放入 assets/manual/ 目录
# cyber_cat.png 等
```

**输出 JSON 示例：**

```json
{
  "visual": {
    "type": "image",
    "source": "assets/manual/cyber_cat.png",
    "effect": "光效闪烁"
  }
}
```

详细文档：[ANNOTATION_GUIDE.md](parser/ANNOTATION_GUIDE.md)

---

### ChatTTS 本地语音引擎

新增 ChatTTS 本地模型支持，相比 edge-tts 更自然、可调音色：

**配置方法（config.yaml）：**

```yaml
tts:
  enabled: true
  provider: "chattts"     # edge / chattts
  # --- ChatTTS 参数 ---
  seed: 2222              # 音色种子（换不同数字试不同声音）
  speed: 5                # 语速 1-9（5=正常）
  oral: 2                 # 口语化程度 0-9
  laugh: 0                # 笑声 0-2
  break_: 4               # 停顿 0-7
```

**声音试听工具：**

```bash
# 运行声音试听工具，测试不同 seed 的音色
python tools/voice_test.py
```

**技术说明：**

- ChatTTS 通过子进程调用离线包自带的 Python 环境，避免 transformers 版本冲突
- 支持 seed 种子调整音色，同一 seed 每次生成的声音一致
- 首次加载模型较慢（约 30-60 秒），后续生成较快

---

## v2.9 特性 — 视觉润色

本次更新专注于提升画面动感与精致度，不引入新的工作流或 CLI 参数，**向后完全兼容**：

### Enhanced Ken Burns（pan + zoom）

所有静态图片场景（`ai_image` / `image` / `clipart` 及 ai_video 兜底图）现在应用真正的 Ken Burns 效果：

- **8 个平移方向**（←→↑↓ + 四对角），由 `scene_id` 哈希稳定决定，同一视频内不同场景各有不同方向
- **15% 缩放**（原 5%），视觉动感提升 3×
- **smoothstep 缓动**：启动和结束柔和，中间段稍快，比线性更自然
- 帧级 PIL LANCZOS 缩放，图像质量无损

### 字幕淡入

字幕不再硬出现，改为 **0.2s FadeIn** 浮现，场景极短时自动收窄至 10% 时长。

### solid_bg 主题配色

LLM 导演现在可以为纯色背景卡指定语义配色：

```json
"visual": {"type": "solid_bg", "prompt": "本质 = LLM", "color": "#0d1b2a"}
```


| 场景语义     | 推荐色           |
| ------------ | ---------------- |
| 科技 / AI    | `#0d1b2a` 深蓝   |
| 结论 / 强调  | `#1e0a3c` 深紫   |
| 数据 / 逻辑  | `#0a2a2a` 深青   |
| 暖场 / 引入  | `#2a1800` 深棕   |
| 默认（不填） | 浅灰渐变（原有） |

深色背景时文字自动切换为白色。`color` 字段可选，缺省完全向后兼容。

### Avatar PiP 软阴影

`pip_br / pip_bl / pip_tr / pip_tl` 模式下，Avatar 图层后方自动添加半透明黑色阴影矩形，使解说人从画面中"浮起来"，增加层次感。

---

## v2.8 特性 — AI 视频双轨模式

本次更新为导演引擎增加了 `--mode` 开关，支持在**纯图片模式**和**AI 视频模式**之间切换：

- **`--mode image`（默认）**：仅使用静态素材（solid_bg / clipart / ai_image / manim），生成图片需求单，供用户自行下载或生成后放置。行为与 v2.7 完全一致。
- **`--mode video`**：导演可额外调度 `ai_video` 类型（每段视频最多 2 个动态镜头），并在需求单中输出完整的 AI 视频生成参数（prompt / duration / motion），用户自行生成后放至 `assets/videos/` 即可。
- **`--director cinematic`**：新增电影质感导演预设，专为 video 模式设计，偏好动态镜头与电影感构图。
- **ai_video 兜底机制**：未放置视频时自动降级为 fallback ai_image，或渲染深色占位卡，构建流程永不中断。

---

## 主推工作流：Avatar 导演模式

**适用场景**：你拥有一段**原始草稿文案**，搭配一段完整的**解说人视频（Avatar）**。你希望系统自动规划分镜、提炼重点、排期画中画并在必要处嵌入图片和动画。

### 极速上手

**Phase 1: 策划 (Plan) — 自动润色 + 导演分镜**

```bash
# 图片模式（默认）：仅使用静态素材
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4

# 图片模式 + 叙事导演
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --director narrative

# AI 视频模式：导演可使用最多 2 个动态 ai_video 镜头
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --mode video

# AI 视频模式 + 电影感导演（推荐搭配）
python pipeline.py plan --project projects/MyVideo --text draft.txt --avatar input/my_avatar.mp4 --mode video --director cinematic
```

> **Plan 的产出：**
>
> 1. `projects/MyVideo/script.json` — 详尽的分镜剧本（画面、音频、转场、布局）
> 2. `projects/MyVideo/script_needs.json` — 精确的需求补单

`script_needs.json` 格式示例：

```json
{
  "visual_mode": "video",
  "ai_image_count": 2,
  "ai_video_count": 1,
  "needs_list": [
    {
      "type": "ai_image",
      "scene_id": "s02",
      "filename": "assets/images/s02.png",
      "description": "futuristic city skyline at night, neon lights, 4k"
    },
    {
      "type": "ai_video",
      "scene_id": "s05",
      "filename": "assets/videos/s05.mp4",
      "description": "[Prompt] data streams flowing through neural networks | Duration: 6s | Motion: slow",
      "prompt": "data streams flowing through neural networks, blue glow, cinematic",
      "duration": 6,
      "motion": "slow"
    }
  ]
}
```

---

**Phase 1.5: 素材准备**

```bash
# 一键批量下载所有 clipart/image 类素材（Pixabay 免费图库）
python scripts/auto_fetch_assets.py --project projects/MyVideo --skip-existing
```

对于 `ai_video` 类型的素材，需根据需求单自行生成并放置：

```text
projects/MyVideo/assets/videos/s05.mp4   ← 按 script_needs.json 中的 filename 字段放置
```

---

**Phase 2: 合成 (Build)**

```bash
python pipeline.py build --project projects/MyVideo
```

> **Build 的产出**：`projects/MyVideo/output/MyVideo.mp4` + `MyVideo.srt`

---

## 导演预设一览 (`--director`)


| 预设               | 风格     | 适合场景                                                                                               |
| ------------------ | -------- | ------------------------------------------------------------------------------------------------------ |
| `standard`（默认） | 均衡稳健 | 通用科普、产品介绍                                                                                     |
| `concept`          | 概念科普 | 逻辑流、分拆图解，偏好 split_screen / Manim                                                            |
| `narrative`        | 激情叙事 | 故事驱动、情感共鸣，快切全屏                                                                           |
| `cinematic`        | 电影质感 | 搭配`--mode video`，2 个 ai_video 配额自由放置在视觉冲击力最强的场景，所有 prompt 采用电影摄影描述语言 |

---

## 目录规范与路径说明

推荐使用**项目目录机制**，框架自动管理所有路径：

```text
projects/
  └── MyVideo/
       ├── draft.txt                  # [输入] 草稿文案（用户提供）
       ├── script.json                # [系统生成] LLM 分镜剧本
       ├── script_needs.json          # [系统生成] 需求清单
       ├── output/
       │    ├── MyVideo.mp4           # [系统生成] 最终成片
       │    └── MyVideo.srt           # [系统生成] 外挂字幕
       └── assets/
            ├── images/               # AI 生图 / 手动放置的图片（{scene_id}.png）
            ├── audio/                # TTS 生成的语音片段
            ├── avatar/               # Avatar 按分镜精准切割的素材库
            └── videos/               # [手动放置] AI 视频文件（{scene_id}.mp4）
```

**多语言变体：**

```bash
python pipeline.py plan --project projects/MyVideo --text draft.txt --lang zh
# 生成: projects/MyVideo/script_zh.json

python pipeline.py plan --project projects/MyVideo --text draft.txt --lang en
# 生成: projects/MyVideo/script_en.json

python pipeline.py build --project projects/MyVideo --lang en
# 读取: projects/MyVideo/script_en.json（缺失则回退到 script.json）
```

**项目清理命令：**

```bash
python cleanup_project.py --project MyVideo          # 安全清理中间层缓存
python cleanup_project.py --project MyVideo --deep   # 深度销毁输出与资源
```

---

## 视觉素材成本优先级

LLM 导演在 `plan` 阶段遵循以下**视觉成本**排序：


| 优先级 | 类型                | 成本 | 说明                                       |
| ------ | ------------------- | ---- | ------------------------------------------ |
| 1      | `title_card`        | 免费 | 片头/片尾标题卡，纯渲染                    |
| 2      | `solid_bg`          | 免费 | 纯色背景板，自动提炼 5-8 字核心词          |
| 3      | `clipart` / `image` | 免费 | 生成英文关键词，引导从 Pixabay/Pexels 获取 |
| 4      | `manim`             | 免费 | 公式、流程图自动转 Manim 动画渲染          |
| 5      | `ai_image`          | 付费 | 每段视频最多 2-3 张，强化视觉冲击          |
| 6      | `ai_video`          | 付费 | 仅`--mode video` 时可用，每段最多 2 个     |

---

## 完整 CLI 参数参考

### `plan` 阶段

```bash
python pipeline.py plan \
  --project  projects/MyVideo    # 项目目录（推荐，路径自动管理）
  --text     draft.txt           # 草稿文案路径（相对项目目录或绝对路径）
  --avatar   input/avatar.mp4   # Avatar 视频（可选，不提供则无解说人）
  --mode     image|video         # 素材模式：image(默认) / video(启用 ai_video)
  --director standard|concept|narrative|cinematic   # 导演风格预设
  --lang     auto|zh|en          # 输出语言（auto 自动检测）
  --output   path/to/script.json # 手动指定脚本输出路径（可选）
```

### `build` 阶段

```bash
python pipeline.py build \
  --project  projects/MyVideo    # 项目目录（与 plan 对应）
  --script   path/to/script.json # 手动指定脚本（与 --project 二选一）
  --lang     zh|en               # 读取语言变体脚本
```

---

## 环境准备与全局配置

### 基础环境

```bash
conda create -n autovideo python=3.10 -y
conda activate autovideo
pip install -r requirements.txt
cp config.example.yaml config.yaml   # 填入各平台 API Key
```

依赖简表：`moviepy`（音画合成）、`manim`（数学动画）、`edge-tts`（微软免费语音）、`openai/httpx`（模型调用）、`pyyaml/rich`（工程化构件）。

**ChatTTS 可选依赖（如需使用本地语音）：**

- ChatTTS 离线包（需自行下载并配置路径）
- 路径配置：`audio/chattts_engine.py` 中的 `CHATTTS_PATH` 变量

### 全局配置 (config.yaml) 概览


| 配置节           | 说明                                                                        |
| ---------------- | --------------------------------------------------------------------------- |
| `llm`            | 导演引擎 LLM，填写 DeepSeek / Qwen 等 API                                   |
| `image_gen`      | AI 生图模型（wan2.6-t2i 等）接口与配额，通过`.api_call_count.json` 管控消耗 |
| `pixabay`        | Pixabay 免费图库 API Key，用于自动下载 clipart/image 素材                   |
| `avatar`         | Avatar 模式默认布局策略（如`pip_br` 右下角）                                |
| `video/subtitle` | 全局输出分辨率、字号安全阈值、默认转场动画时长                              |

---

## 向下兼容：v1 基础组装模式

适合：**没有 Avatar 录像**，只需 TTS 配音 + 静态生图拼接的极简解说短视频。

```bash
# 1. 生成 JSON 剧本
python parser/script_converter.py scripts/my_video.txt

# 2. 从 JSON 剧本合成
python pipeline.py build --script scripts/my_video.json
```

---

## 服务器部署避坑指南（无 sudo 权限）

### 1. 局部接管系统级依赖

```bash
conda activate autovideo
conda install -c conda-forge ffmpeg imagemagick -y
```

### 2. 绕过 ImageMagick 安全封锁（必做）

```bash
mkdir -p ~/.config/ImageMagick
cat << 'EOF' > ~/.config/ImageMagick/policy.xml
<policymap>
  <policy domain="path" rights="read" pattern="@*" />
</policymap>
EOF
```

### 3. 中文字体自动化

Linux 默认缺失中文字库，导致满屏"豆腐块"：

```bash
# 自动拉取字体到 assets/fonts/（无需 sudo）
python scripts/download_fonts.py
```

`config.yaml` 中的 `font: "Microsoft-YaHei"` 会在运行时自动检索 `assets/fonts/` 目录加载，全程无需 sudo 权限。
