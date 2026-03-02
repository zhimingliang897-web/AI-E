# AutoVideo 变更日志

从零开始的完整技术演进记录，方便回顾整个项目的开发历程。

---

## v3.0 - 标注模式 + ChatTTS

**目标**: 支持用户在 txt 文案中标注自备素材和特效，LLM 原样保留；新增 ChatTTS 本地语音引擎。

### 新功能

#### 用户标注转换器（独立模块）

**新增文件**: `parser/annotated_converter.py`

独立的文案转换器，专门处理带标注的 txt 文案，与现有 `script_converter.py` 并行存在：

- **图片/视频标注** `[xxx.png]` `[xxx.mp4]`
  - 自动识别为用户自备素材
  - `visual.type` 设为 `"image"` 或 `"video"`
  - `visual.source` 设为 `"assets/manual/xxx.png"`
  - LLM 不会用 ai_image 替换

- **特效标注** `{特效：描述}` `{特效:描述}`
  - 存入 `visual.effect` 字段
  - 供后续特效处理使用（预留扩展点）

- **画面/配音分离** `【画面】...【配音】...`
  - 【画面】段落的内容用于画面描述，不会被 TTS 朗读
  - 【配音】段落的内容会被拆分成多个场景并朗读

**运行命令**:
```bash
python -m parser.annotated_converter my_script.txt -o script.json --avatar
```

**新增文件**: `parser/ANNOTATION_GUIDE.md`

详细的标注格式使用指南，包含语法说明、示例和注意事项。

---

#### ChatTTS 本地语音引擎

**新增文件**: `audio/chattts_engine.py`

支持 ChatTTS 本地模型，相比 edge-tts 更自然、可调音色：

- **子进程隔离**: 通过子进程调用 ChatTTS 离线包自带的 Python 环境，避免 transformers 版本冲突
- **音色种子**: `seed` 参数决定音色，同一 seed 每次生成一致
- **参数配置**: 支持 speed（语速）、oral（口语化）、laugh（笑声）、break_（停顿）

**配置方法** (`config.yaml`):
```yaml
tts:
  provider: "chattts"     # edge / chattts
  seed: 2222              # 音色种子
  speed: 5                # 语速 1-9
  oral: 2                 # 口语化 0-9
  laugh: 0                # 笑声 0-2
  break_: 4               # 停顿 0-7
```

**修改文件**: `config.py`

`TTSConfig` 新增字段：
- `provider: str = "edge"` - TTS 引擎选择
- `seed: int = 2222` - ChatTTS 音色种子
- `speed: int = 5` - ChatTTS 语速
- `oral: int = 2` - ChatTTS 口语化程度
- `laugh: int = 0` - ChatTTS 笑声程度
- `break_: int = 4` - ChatTTS 停顿程度

**修改文件**: `pipeline.py`

TTS 阶段根据 `provider` 字段选择引擎：
- `edge`: 使用 edge-tts（默认）
- `chattts`: 使用 ChatTTS 本地模型

---

#### 声音试听工具

**新增/更新文件**: `tools/voice_test.py`

交互式声音试听工具，支持测试 edge-tts 和 ChatTTS：

- **edge-tts**: 可选声音列表 + 语速调节
- **ChatTTS**: 预设种子 / 自定义种子 + 语速调节
- **播放模式**: 生成后逐个播放，方便对比

**运行命令**:
```bash
python tools/voice_test.py
```

### 修改的文件汇总

| 文件 | 改动 |
|---|---|
| `parser/annotated_converter.py` | **新增**：带标注的文案转换器 |
| `parser/ANNOTATION_GUIDE.md` | **新增**：标注格式使用指南 |
| `audio/chattts_engine.py` | **新增**：ChatTTS 本地语音引擎 |
| `config.py` | TTSConfig 新增 provider、seed、speed、oral、laugh、break_ 字段 |
| `config.yaml` | 新增 ChatTTS 配置节 |
| `pipeline.py` | TTS 阶段支持 chattts provider |
| `tools/voice_test.py` | 支持 ChatTTS 声音试听 |
| `README.md` | v3.0 版本文档 |

---

## v2.9 - 视觉润色

**目标**: 专项提升画面动感与精致度，不引入新 CLI 参数，向后完全兼容。

### 新功能

#### Enhanced Ken Burns：pan + zoom（`compositor/assembler.py`）

- **新增 `_apply_ken_burns(path, width, height, duration, scene_id)`**：替代原来仅有 5% 纯缩放的静态效果。
- **8 个平移方向**：←→↑↓ 及四对角（TL↔BR、TR↔BL），由 `scene_id` 的 MD5 哈希低位决定，同一视频内各场景方向稳定且各不相同。
- **15% zoom**（原 5%），视觉动感提升约 3×。
- **smoothstep 缓动**：进度曲线 `p = p²(3-2p)`，启动/结束平滑，中间段稍快，比线性更自然。
- **实现方式**：图像一次性预放大至 130%（numpy 数组），每帧按 (pan_x, pan_y, zoom) 裁剪并 PIL LANCZOS 缩回输出尺寸，无质量损失。
- **应用范围**：`ai_image`、`image`、`clipart`、`ai_video` 兜底图（fallback_img），统一调用同一函数。
- **新增导入**：`VideoClip`（moviepy）。

#### 字幕淡入动画（`compositor/assembler.py`）

- `_make_subtitle_clip()` 返回值加 `vfx.FadeIn(fade_dur)`，默认 **0.2s**。
- 场景极短时自动收窄：`fade_dur = min(0.2, duration * 0.1)`，保证不超出场景时长。
- 字幕由"硬出"改为"浮现"，视觉节奏更顺滑。

#### solid_bg 主题配色（多文件）

- `script.json` 的 `solid_bg` 场景 visual 对象支持可选 `color` 字段（hex，如 `"#0d1b2a"`）。
- `parser/script_parser.py`：`SceneItem` 新增 `visual_color: Optional[str]`，解析 `visual.get("color")`（仅 solid_bg 生效）。
- `compositor/assembler.py`：solid_bg 渲染时读取 `scene.visual_color`，有值则以该色为顶色、-18 为底色渐变，文字自动切白；无值则回退浅灰渐变 + 深灰文字（原行为）。
- `parser/script_converter.py`：两个 SYSTEM_PROMPT（标准 + video 模式）均补充 solid_bg 配色说明，推荐色盘：科技深蓝 `#0d1b2a`、结论深紫 `#1e0a3c`、逻辑深青 `#0a2a2a`、暖场深棕 `#2a1800`。

#### Avatar PiP 软阴影（`compositor/assembler.py`）

- `_overlay_avatar()` 的 `pip_*` 分支合成前插入半透明阴影层：
  - `ColorClip(size=(pip_w+24, pip_h+24), color=(0,0,0))` + `with_opacity(0.45)`
  - 合成顺序：`base_clip → shadow → avatar_clip`
- Avatar 从平贴画面变为"浮起"效果，层次感显著增强。

### Bug 修复

#### script_parser.py 路径检查误报（`parser/script_parser.py`）

- **问题**：`parse_script` 中的存在性检查使用相对于进程 cwd 的路径，而 `set_project_dir` 只更新 cfg 路径变量，不改 cwd，导致 ai_video 素材路径始终 warn"不存在"。
- **修复**：检查时以脚本文件所在目录（项目目录）为基准解析相对路径：`os.path.join(script_base_dir, scene.visual_source)`，与 assembler 实际加载行为对齐，消除误报。
- **同步修复**：手动音频路径（`audio_override`）同样改为以 `script_base_dir` 为基准校验。

### 修改的文件汇总

| 文件 | 改动 |
|---|---|
| `compositor/assembler.py` | `VideoClip` 导入 + `_apply_ken_burns()` 函数 + 3 处图片场景替换调用 + 字幕淡入 + solid_bg 配色 + PiP 阴影 |
| `parser/script_parser.py` | `SceneItem.visual_color` 字段 + `visual.color` 解析 + 路径检查 bug 修复 |
| `parser/script_converter.py` | SYSTEM_PROMPT / SYSTEM_PROMPT_VIDEO 中 solid_bg 配色说明 |
| `README.md` | v2.9 特性文档 |

---

## v2.8 - AI 视频双轨模式

**目标**: 在保持原有图片模式完整功能的基础上，增加 ai_video 类型支持，通过 `--mode` 开关实现两套独立工作流。

### 新功能

#### `--mode {image,video}` 双轨切换
- `plan` 阶段新增 `--mode` 参数（默认 `image`）：
  - `image` 模式：行为与 v2.7 完全一致，仅使用静态素材。
  - `video` 模式：导演可使用 `ai_video` 类型，每段视频最多 2 个，需求单自动输出 ai_video 条目（含 prompt / duration / motion）。
- **文件**: `pipeline.py`

#### `ai_video` 视觉类型
- `VALID_VISUAL_TYPES` 新增 `"ai_video"`。
- 解析逻辑：source 优先取 `visual.source`，缺省则自动补 `assets/videos/{scene_id}.mp4`；`visual_prompt` 透传 `visual.prompt`。
- 存在性检查：与 `image/video` 同等对待，缺失时输出 warn。
- **文件**: `parser/script_parser.py`

#### `SYSTEM_PROMPT_VIDEO`（video 模式专用导演 prompt）
- 新增独立 prompt 常量，在 `visual_mode == "video"` 时替换默认 prompt。
- 明确 ai_video 使用规则：全视频最多 2 个、必须含运动描述（falling/flowing/rotating...）、duration 4-8s、motion slow/medium/fast、必须填写 fallback。
- **文件**: `parser/script_converter.py`

#### `_rebalance_ai_video_cost` 防御性重平衡
- 在 `_rebalance_visual_cost` 之后执行：
  - `image` 模式：将所有 ai_video 强制降级为 ai_image（使用 fallback prompt），防止 LLM 幻觉。
  - `video` 模式：保留前 2 个，其余降级。
- **文件**: `parser/script_converter.py`

#### needs_list 新增 ai_video 条目
- `_build_needs_list` 返回值扩展为 `(needs, ai_image_count, ai_video_count)`。
- ai_video 条目包含：`filename`（`assets/videos/{sid}.mp4`）、`description`（含 Prompt/Duration/Motion）、`prompt`、`duration`、`motion`。
- `script_needs.json` 新增顶层字段 `ai_video_count` 和 `visual_mode`。
- **文件**: `parser/script_converter.py`

#### assembler.py ai_video 加载（三级兜底）
- 第 1 级：加载 `assets/videos/{scene_id}.mp4`，短于 duration 时自动 loop（`vfx.Loop`），长于则截断。
- 第 2 级：视频缺失时尝试 `assets/images/{scene_id}_fallback.png`，缩放动画同 ai_image。
- 第 3 级：两者均缺失时渲染深色渐变占位卡（"[AI Video Pending]"），build 流程永不中断。
- **文件**: `compositor/assembler.py`

#### `--director cinematic` 预设
- 新增第 4 种导演预设，专为 video 模式设计。
- 指令：2 个 ai_video 配额自由放置在视觉冲击力最强的场景（不限位置），所有视觉 prompt 使用电影级摄影描述语言，Avatar 优先 fullscreen 或 hidden。
- **文件**: `pipeline.py`

### 修改的文件汇总

| 文件 | 改动 |
|---|---|
| `parser/script_parser.py` | ai_video 加入 VALID_VISUAL_TYPES + source 提取 + 存在性检查 |
| `parser/script_converter.py` | SYSTEM_PROMPT_VIDEO + _rebalance_ai_video_cost + needs_list ai_video 条目 + convert_text_to_json visual_mode 参数 |
| `pipeline.py` | --mode 参数 + --director cinematic + visual_mode 透传 |
| `compositor/assembler.py` | ai_video 三级兜底加载逻辑 |
| `README.md` | v2.8 版本文档（双轨模式、目录结构、CLI 参数表） |

---

## v2.7 - 导演引擎升级 + 跨话题泛化

**目标**: 从"AI/LLM 题材优先"升级为多领域通用导演策略，并增加动态导演预设以控制视频节奏感。

### 新功能

#### `--director` 导演风格预设
- `plan` 阶段新增 `--director` 参数，支持 3 种预设（`standard` 为默认）：
  - `concept`：概念科普向，频繁使用 split_screen，以 manim + solid_bg 构建逻辑流。
  - `narrative`：激情叙事向，快速切换，大量全屏 ai_image 强化情感冲击。
- 实现机制：通过在文本前注入 `[DIRECTOR_NOTES]` 区块，让 LLM 在生成分镜时看到导演风格要求。
- **文件**: `pipeline.py`

#### `--domain` 话题领域参数
- 新增 `--domain` 参数（`auto/tech/business/science/education/health/history/law/lifestyle`）。
- 自动推断话题标签并注入 LLM，约束视觉提示词语义与领域一致，禁止强行套 AI 语境。
- **文件**: `pipeline.py`, `parser/script_converter.py`

#### Avatar 自动循环防定格
- 当 Avatar 解说素材时长短于场景旁白时，自动启用 `vfx.Loop` 平滑循环。
- 修复"最后一帧静止定格"的视觉僵硬问题。
- **文件**: `compositor/assembler.py`

#### solid_bg 关键词严格提炼
- 导演规则强制要求 `solid_bg` 背景板提炼 5-8 字核心词，禁止直接复制旁白整句。
- 避免屏幕信息冗余，提升视觉精炼度。
- **文件**: `parser/script_converter.py`（SYSTEM_PROMPT）

#### needs_list 精准英文关键词
- LLM 在 `description` 字段中强制生成纯英文 Keyword（如 `business, startup, chart`）。
- 便于后续用 Pixabay/Pexels 精准搜索免费素材。
- **文件**: `parser/script_converter.py`

#### 无音频标题卡时长优化
- 无配音 `title_card` 默认停留时长提升至 **3.0s**（之前 1.2s），保障观众阅读时间。
- **文件**: `compositor/assembler.py`

### 稳定性增强

#### 成本重平衡策略增强
- 强叙事关键词支持中英文（如 `开场/summary/conclusion`）。
- 短句判断改为中英文自适应（不再只按中文字符长度）。
- `_looks_formula_scene` 扩展更多中英文关键词。
- **文件**: `parser/script_converter.py`

---

## v2.6 - 逐场景转场 + 导演策略增强

**目标**: 让场景过渡更可控、txt→json 更稳、并降低付费 AI 生图依赖。

### 新功能

#### 逐场景 transition 生效
- **修复前**: 合成阶段主要按全局 `video.transition` 处理，场景里的 `transition` 字段控制力有限。
- **修复后**: 采用"逐场景转场"拼接：
  - `scene[i].transition` 作用于 `scene[i] -> scene[i+1]`
  - 支持 `crossfade / fade_black / cut` 混用
  - 无效值自动回退到全局默认转场
- **文件**: `compositor/assembler.py`

#### txt → json 规范化增强
- 新增输入清洗：自动处理 Markdown 标题、列表符号、空行和代码块，减少"格式不规范 txt"对 LLM 输出结构的影响。
- 新增场景后处理：统一补全字段、修正非法类型、去重并规范 scene id、纠正无效 transition/audio/avatar 值。
- **文件**: `parser/script_converter.py`

#### 低成本视觉策略强化
- 导演规则改为优先 `clipart/image/manim/solid_bg`，`ai_image` 仅少量用于关键镜头。
- 新增自动重平衡逻辑：若 `ai_image` 过多，会自动降级为 `clipart/solid_bg/manim` 并补 needs_list。
- needs_list 统一去重并补全文件名，默认推荐免费开源插画来源。
- **文件**: `parser/script_converter.py`

### 稳定性修复

#### Manim 自动生成 prompt 透传修复
- `SceneItem` 新增 `visual_prompt`，`parse_script` 透传 `visual.prompt`。
- `manim_renderer` 生成缺失场景代码时可稳定拿到 prompt，不再依赖不存在字段。
- **文件**: `parser/script_parser.py`, `visuals/manim_renderer.py`

---

## v2.5 - 开场优化 + 字体调优 + 清理整理

**目标**: 解决开场"黑屏偏长"、标题/字幕可读性、以及项目中间文件堆积问题。

### Bug 修复

#### title_card 未读取 prompt 导致黑底无标题
- **问题**: `script_parser.py` 对 `title_card` 只读 `visual.source`，忽略 `visual.prompt`，导致标题卡只有黑底。
- **修复**: `title_card` 与 `solid_bg/ai_image` 一样优先读取 `prompt` 字段。
- **文件**: `parser/script_parser.py`

### 体验优化

#### 开场黑屏时长优化
- **问题**: 标题卡无音频时会按普通场景默认时长（2.5s）停留，开场显得拖沓。
- **修复**: 无音频 `title_card` 默认时长改为 **1.2s**（`solid_bg` 仍为 1.5s）。
- **文件**: `compositor/assembler.py`

#### title_card 视觉优化
- **问题**: 纯黑底压感较强，开头观感偏闷。
- **修复**: `title_card` 背景改为暗色渐变（保留章节卡风格，减轻纯黑压屏感）。
- **文件**: `compositor/assembler.py`

#### 默认字体参数调优（1080p）
- `subtitle.font_size`: 32 → 36
- `subtitle.title_font_size`: 56 → 64
- `subtitle.bg_opacity`: 0.5/0.6 → 0.55
- **文件**: `config.py`, `config.yaml`, `config.example.yaml`

### 工程整理

#### 新增清理脚本
- 新增 `cleanup_project.py`，支持：
  - 安全清理（debug 文件、测试输出、`__pycache__`）
  - `--project` 指定项目
  - `--deep` 深度清理项目生成产物
  - `--dry-run` 预览

#### 删除历史一次性修复脚本
- 删除：`diagnose_*.py`, `fix_*.py`, `parser/test_fix.py`

---

## v2.2 - 路径 Bug 修复 + 文档对齐

**目标**: 修复 `config.py` 的路径双重叠加 bug，并将文档与实际项目模式对齐。

### Bug 修复

#### config.py 路径 double-resolve
- **问题**: `load_config()` 中 `cfg.paths.resolve(BASE_DIR)` 被连续调用两次，导致非项目模式下路径变成 `BASE_DIR/BASE_DIR/assets`（双重叠加）。
- **影响**: 使用 `--script` 而非 `--project` 时，assets/output 路径错误（项目模式因 `set_project_dir` 覆盖路径不受影响）。
- **修复**: 删除重复的第二次 `cfg.paths.resolve(BASE_DIR)` 调用。
- **文件**: `config.py`

---

## v2.1 - Windows 稳定性修复 + 标题卡优化

**目标**: 修复 number2 项目首次 build 中暴露的一系列兼容性问题，让 pipeline 在 Windows 上稳定端到端运行。

### Bug 修复

#### Rich Console GBK 编码崩溃
- **问题**: Windows 终端使用 GBK 编码，Rich 遇到 `\xa0`（不间断空格）时报 `UnicodeEncodeError`。
- **修复**: Console 初始化时强制包装 `sys.stdout.buffer` 为 UTF-8 编码的 `TextIOWrapper`。
- **文件**: `pipeline.py`

#### 空 MP3 文件导致 AudioFileClip 崩溃
- **问题**: TTS 对标题场景（无文本）生成了 0 字节的 `.mp3`，`AudioFileClip` 打开时 ffmpeg 报 `Invalid data found`。
- **修复**: 在 3 处加入 `os.path.getsize() > 0` 检查：`avatar/splitter.py`、`compositor/assembler.py`、`subtitles/srt_generator.py`。

#### Windows 临时音频文件 PermissionError
- **问题**: moviepy 的 `write_videofile(remove_temp=True)` 在 Windows 上删除临时音频文件时被进程占用，报 `[WinError 32]`。
- **修复**: 改为 `remove_temp=False`，在 `finally` 块中手动清理（静默忽略 PermissionError）。
- **文件**: `compositor/assembler.py`

### 新功能

#### 标题卡文字渲染
- `solid_bg` 类型场景从 `visual.prompt` 读取标题文字，以 72px 深色粗体居中渲染在渐变背景上，形成章节分隔卡。
- 标题场景（无文本 + solid_bg）缩短为 1.5 秒。
- **文件**: `compositor/assembler.py`, `parser/script_parser.py`

#### 字幕位置与换行重写
- 改用 `TextClip(method="caption", size=(max_w, None))`，由 PIL 自动换行。
- 字幕位置固定在画面 75% 高度（底部保留 25% 安全区）。
- 移除手动估算字符宽度的 `_wrap_text_to_width()` 函数。
- **文件**: `compositor/assembler.py`

---

## v2 - Avatar 导演模式

**目标**: 支持动画小人叠加、LLM 智能导演、字幕烧入、视觉质量提升。

### 新增文件
- `avatar/splitter.py` - Avatar 视频按场景时长切割器

### 核心改动

#### script_converter.py - 导演级 SYSTEM_PROMPT
- 视觉策略优先级：solid_bg > clipart/image > manim > ai_image（省钱策略）
- Avatar 布局规则：开场 fullscreen、讲解 pip_br、展示 hidden
- 输出 `needs_list`（素材清单）+ `ai_image_count` + `summary`
- 保留 `SYSTEM_PROMPT_V1`（向后兼容简单模式）

#### compositor/assembler.py - 核心改造
- 渐变背景：`_make_gradient_bg()` 替代纯黑，深蓝渐变
- Avatar 叠加：支持 fullscreen / pip_br/bl/tr/tl / split_left/right 6 种布局
- 字幕烧入：半透明底条 + 白色文字 + TextClip
- 场景转场：crossfade / fade_black / cut

#### pipeline.py - 两阶段重构
- `plan` 子命令：调用 LLM 导演生成 script.json + needs_list
- `build` 子命令：7 步流程（+Avatar 切割）
- 向后兼容：`python pipeline.py --script xxx.json` 等同 build

### JSON Schema 变化

```
v1 字段:
  id, text, visual{type,prompt,scene_class,source,fallback}, audio{mode,override}

v2 新增字段:
  avatar{mode,scale}, transition
  visual.type 新增: solid_bg, clipart
  audio.mode 新增: avatar
```

---

## v1 - 基础定位润色

**目标**: 修复首次运行中的各种兼容性问题，让 pipeline 可以端到端跑通。

### Bug 修复

- **Manim 输出路径找不到**: `manim_renderer.py` 搜索 3 个目录（cwd → scenes_file 目录 → 项目根目录）
- **MoviePy v2 ImageClip 无 color 参数**: 改用 `numpy.full((h,w,3), ...)` 生成纯色数组
- **DashScope 404/400/403/字段名**: 经历 4 轮调试，最终改用原生 REST API，区分 wan2.6 和 wanx-v1 两套端点

### 新增
- `parser/script_converter.py` - LLM 文案转 JSON 工具
- API 调用计数器（`.api_call_count.json`）+ `max_calls` 额度限制

---

## v0 - 初始版本

**目标**: 建立项目骨架和基础 pipeline。

### 创建的文件
- `config.py` - dataclass 配置系统
- `parser/script_parser.py` - JSON 剧本解析器，SceneItem dataclass
- `audio/tts_engine.py` - edge-tts 异步配音
- `audio/rvc_engine.py` - RVC WebUI HTTP API 变声
- `visuals/manim_scenes.py` - 示例 Manim 场景
- `visuals/manim_renderer.py` - subprocess 调用 manim CLI 渲染
- `visuals/image_gen.py` - AI 图片生成（OpenAI 兼容接口）
- `compositor/assembler.py` - MoviePy 音画合成（Ken Burns 缩放效果）
- `subtitles/srt_generator.py` - SRT 外挂字幕生成
- `pipeline.py` - 6 步主控 CLI

### 技术选型
- conda 环境 Python 3.10（兼容 RVC + manim + moviepy）
- MoviePy v2（非 v1），API 完全不同
- edge-tts 微软免费 TTS
- DashScope 阿里云 API，兼容 OpenAI 格式（部分接口）

---

## 技术备忘

### DashScope API 要点
- 文生图**不走** OpenAI 兼容接口，必须用原生 REST API
- wan2.6 系列：`multimodal-generation/generation` 端点 + messages 格式
- wanx-v1：`text2image/image-synthesis` 端点 + prompt 格式
- 同步调用，不加 `X-DashScope-Async` header
- 响应图片 URL 字段可能是 `image` 或 `image_url`，都要检查

### MoviePy v2 要点
- `ImageClip(color=...)` → numpy 数组
- `clip.resize()` → `clip.resized()`
- `clip.set_duration()` → `clip.with_duration()`
- `clip.set_audio()` → `clip.with_audio()`
- `clip.subclip()` → `clip.subclipped()`
- 特效：`clip.with_effects([vfx.Xxx()])`
- 叠加：`CompositeVideoClip([base, overlay.with_position((x,y))])`

### Windows 特殊处理
- `conda run` 中文输出 GBK 报错 → 直接用 python.exe 路径
- 字幕字体用 `Microsoft-YaHei`（Windows 自带微软雅黑）
- Rich Console 需要 `io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")`
- moviepy `remove_temp=True` 在 Windows 会 PermissionError → 用 `remove_temp=False` + 手动清理
- 空音频文件（0 字节 mp3）会导致 ffmpeg 崩溃 → 所有读取音频处需检查文件大小
