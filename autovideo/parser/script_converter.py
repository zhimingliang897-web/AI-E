"""文案 → JSON 转换器 - 用 LLM 智能导演将纯文本脚本转为 pipeline 所需的 JSON 格式"""

import json
import os
import sys
import re
from typing import Any

from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import load_config
from parser.script_parser import (
    VALID_AUDIO_MODES,
    VALID_AVATAR_MODES,
    VALID_TRANSITIONS,
    VALID_VISUAL_TYPES,
)

# ===== v2 导演级 SYSTEM_PROMPT（图片模式，无 ai_video）=====
SYSTEM_PROMPT = """你是一个专业视频导演 AI。用户会给你一段视频文案（可能是草稿，包含格式混乱、加粗、错别字等），你需要：
1. **尊重原文，仅限纠错**：用户的短文案基本是定稿，**严禁大篇幅改写或擅自精简段落**。你只能在此基础上修复明显的语法错误、去除 Markdown 格式（如 **加粗**）、让口语更通顺，保持原有的讲解节奏和核心意思完全不变。
2. 拆分成多个场景
3. 为每个场景选择最合适的视觉策略和 Avatar 布局
4. 输出需求清单（用户需要准备的素材）

## 输出格式（严格 JSON）

```json
{
  "scenes": [
    {
      "id": "01_intro",
      "text": "旁白文案",
      "visual": {
        "type": "solid_bg | clipart | image | manim | ai_image | video",
        "prompt": "英文图片描述（仅 ai_image 时填）",
        "source": "assets/manual/xxx.png（仅 image/video/clipart 时填）",
        "scene_class": null,
        "fallback": null
      },
      "avatar": {
        "mode": "pip_br | pip_bl | pip_tr | pip_tl | fullscreen | split_left | split_right | hidden",
        "scale": 0.3
      },
      "audio": {
        "mode": "auto",
        "override": null
      },
      "transition": "crossfade | fade_black | cut"
    }
  ],
  "needs_list": [
    {"scene_id": "05_chart", "type": "image", "filename": "assets/manual/05_chart.jpg", "description": "需要一张 XXX 的图片/截图。关键词：business, chart, growth"}
  ],
  "ai_image_count": 2,
  "summary": "共N个场景，需要AI生图X张，需要你准备Y张图片"
}
```

## 视觉策略选择规则（重要！按优先级从高到低）

1. **title_card** (黑底标题卡): **遇到 `=== 标题 ===` 时必须使用**。
   - 视觉：纯黑背景 + 白色大文字（居中）。
   - text 字段填 ""（空字符串，不读出声音）。
   - visual.prompt 填标题内容，但**必须包含中文翻译**！
     例如：visual.prompt = "概念与举例\nConcepts & Examples"（中文在前，英文在后，用换行分隔）。
   - visual.type 填 "title_card"。
   - avatar.mode 填 "hidden"。
   - **注意**：标题场景默认显示时间为 3.0 秒（以保证观众有充足的阅读时间）。

2. **clipart/image** (优先，免费/低成本):
   - 优先使用开源免费素材思路：OpenMoji / unDraw / Storyset / SVG Repo / Wikimedia Commons / PublicDomainVectors。
   - `visual.type` 用 `clipart` 或 `image`，`visual.source` 指向 `assets/manual/{scene_id}.png`（由 needs_list 提示用户准备）。

3. **manim** (优先，免费):
   - 明确的数学公式、逻辑流程、结构图，优先用 manim。
   - **重要**：如果预定义的类不够用，你可以**创造新的 class 名**（如 `RelativityFormula`）。
   - **必须**在 `visual.prompt` 中详细描述画面内容（例如 "Show E=mc^2 formula with a glowing box around it"），以便我们在后续步骤自动生成代码。

4. **solid_bg** (纯色背景): 用于过渡句、总结、强调结论。
   - **重要**：`visual.prompt` 必须是对当前长句旁白的**高度提炼（不超过 5-8 个字的精准关键词或短语）**。绝对不要原样复制旁白文本！例如旁白为"它们本质都是 LLM"，prompt 应为"本质 = LLM"。
   - **可选配色**：可以在 visual 中加 `"color"` 字段（hex），根据场景语义选色：科技/AI → `"#0d1b2a"`（深蓝）；结论/强调 → `"#1e0a3c"`（深紫）；数据/逻辑 → `"#0a2a2a"`（深青）；暖场/引入 → `"#2a1800"`（深棕）；默认留空（浅灰）。

5. **ai_image** (成本较高，少量使用):
   - 仅用于开场冲击镜头、关键转折或抽象概念无法用免费素材表达的场景。
   - 建议每 10 个场景最多 2~3 个 `ai_image`。
   - 风格提示词加：high quality 3D realistic cartoon style, bright, clean, easy to understand。绝对不要使用抽象、华而不实的科幻设定。

## 拆分规则 (非常重要！)

1. **细粒度拆分**：为了字幕易读，**一句话如果超过 15 个字，必须拆成两个场景**。
   - 错误： "不管是你每天用的 ChatGPT、Gemini，还是国内的通义千问、豆包——它们本质都是 LLM。" (太长！)
   - 正确：
     - Scene 1: "不管是你每天用的 ChatGPT、Gemini，" (visual: ai_image relevant icons)
     - Scene 2: "还是国内的通义千问、豆包——" (visual: ai_image china tech)
     - Scene 3: "它们本质都是 LLM。" (visual: solid_bg + avatar)
2. **节奏感**：动静结合，优先交替使用 clipart/image、manim、solid_bg；ai_image 只点缀。

## Avatar 布局规则

- 讲知识点/展示图片时：**hidden** (让用户看图)。
- 过渡/总结/简单对话时：**pip_br** (画中画) 或 **split_right**。
- **遇到 title_card 必须 hidden**。

## 需求清单生成规则 (最新要求)
- `needs_list` 中如果指明需要 `image` 或 `clipart`，其 `description` 字段必须包含**准确的单排英文搜索关键词（Keywords）**。例如 "需要一张表示启动的图片，关键词：startup, rocket, boost"。不要只给模糊的中文说明，以便后续自动化按关键词去无版权图库精准搜图。

## 重要

- 只输出 JSON 对象。
- visual.prompt 对于 ai_image 必须用英文，并充满想象力；对 solid_bg，提炼精简中文词组即可。
- 输出务必规范，字段齐全，不能缺 key。"""


# ===== v2 导演级 SYSTEM_PROMPT_VIDEO（视频模式，含 ai_video）=====
SYSTEM_PROMPT_VIDEO = """你是一个专业视频导演 AI。用户会给你一段视频文案（可能是草稿），你需要：
1. **尊重原文，仅限纠错**：用户的短文案基本是定稿，**严禁大篇幅改写或擅自精简段落**。你只能在此基础上修复明显的语法错误、去除 Markdown 格式、让口语更通顺，保持原有的讲解节奏和核心意思完全不变。
2. 拆分成多个场景（细粒度，每场景旁白 ≤15 个字）
3. 为每个场景选择最合适的视觉策略（**可使用 ai_video**）和 Avatar 布局
4. 输出需求清单（用户需要手动生成或准备的所有素材）

## 输出格式（严格 JSON）

```json
{
  "scenes": [
    {
      "id": "01_intro",
      "text": "旁白文案（TTS 读出的内容）",
      "visual": {
        "type": "solid_bg | clipart | image | manim | ai_image | ai_video | video",
        "prompt": "描述文字（规则见下方）",
        "source": "assets/manual/xxx.png（仅 image/video/clipart 时填）",
        "scene_class": null,
        "duration": null,
        "motion": null,
        "fallback": null
      },
      "avatar": {
        "mode": "pip_br | pip_bl | pip_tr | pip_tl | fullscreen | split_left | split_right | hidden",
        "scale": 0.3
      },
      "audio": {
        "mode": "auto",
        "override": null
      },
      "transition": "crossfade | fade_black | cut"
    }
  ],
  "needs_list": [
    {"scene_id": "05_chart", "type": "image", "filename": "assets/manual/05_chart.jpg", "description": "需要一张 XXX 的图片。Keywords: business, chart, growth"},
    {"scene_id": "08_climax", "type": "ai_video", "filename": "assets/videos/08_climax.mp4", "description": "[Prompt] Slow motion water droplets... | Duration: 6s | Motion: slow"}
  ],
  "ai_image_count": 2,
  "ai_video_count": 1,
  "summary": "共N个场景，AI视频Y个，AI生图X张，需要你准备Z项素材"
}
```

## 视觉策略选择规则（严格按优先级从高到低）

### 第一优先：免费素材组

**1. title_card** （黑底标题卡）
- 触发条件：遇到 `=== 标题 ===` 标记时**必须使用**。
- text 填 ""（不读旁白）。
- visual.prompt 填标题内容，中文在前+英文在后（换行分隔）。
- avatar.mode 必须 "hidden"，transition 用 "fade_black"。
- 默认显示 3.0 秒。

**2. manim** （代码动画，免费）
- 触发条件：涉及数学公式、逻辑流程、对比结构、数据变化、文字变换效果。
- visual.scene_class 填驼峰命名的类名（如 `AttentionMechanism`），可以创造新名字。
- visual.prompt 用英文详细描述画面（供自动生成代码用）。

**3. solid_bg** （渐变纯色背景 + 关键词）
- 触发条件：过渡句、总结句、强调结论。
- visual.prompt **必须是 5-8 字精准关键词**，绝对不要复制旁白！
- 例：旁白"它们的本质都是大语言模型" → prompt "本质 = LLM"
- **可选**：在 visual 中加 `"color"` 字段（hex），根据场景语义选色：科技/AI → `"#0d1b2a"`（深蓝）；结论/强调 → `"#1e0a3c"`（深紫）；数据/逻辑 → `"#0a2a2a"`（深青）；暖场/引入 → `"#2a1800"`（深棕）；默认留空（浅灰）。示例：`"visual": {"type": "solid_bg", "prompt": "本质 = LLM", "color": "#0d1b2a"}`

**4. clipart/image** （用户准备的免费素材）
- visual.type 填 "clipart" 或 "image"，source 填 "assets/manual/{scene_id}.png"。
- needs_list 给出精准英文搜索关键词（供自动搜图）。

### 第二优先：AI 生图（付费 $，每视频 ≤ 3 张）

**5. ai_image** （AI 静态图）
- 触发条件：开场冲击镜头、角色/场景概念建立、静态象征画面。
- 上限：每 10 个场景最多 2-3 张。
- visual.prompt 必须英文，描述构图+主体+风格。主体越具体越好。
- 风格词：`high quality 3D realistic cartoon style, bright, clean, easy to understand`。绝对不要使用抽象、华而不实的设定。

### 第三优先：AI 视频（付费 $$，全视频 ≤ 2 个）

**6. ai_video** （AI 生成动态视频片段）
- **使用条件（满足任一即可，但全视频总计 ≤ 2 个）**：
  - 情绪峰值：叙事最高潮、最震撼的观点揭示
  - 动态自然过程：水流、火焰、星云、细胞分裂、城市延时、人群
  - 抽象动态概念：神经信号传播、信息流动、量子涨落
  - 电影级运镜：慢镜头特写、镜头拉远揭示、环绕镜头
- **禁止在以下情况使用**：
  - 需要精确文字/数字/图表 → 用 manim
  - 短暂过渡句 → 用 solid_bg
  - 已使用 2 个 ai_video 的视频中继续添加
- **字段规范**：
  - visual.prompt：英文，**必须同时包含**：①画面具体主体 ②运动方式 ③风格（必须是写实卡通）。越接地气、越具体越好，不要花里胡哨。
    - 好例：`"A cute 3D cartoon robot happily sorting colorful blocks on a bright clean table, smooth animation, realistic lighting"`
    - 好例：`"A 3D cartoon scientist looking through a microscope in a bright colorful lab, joyful expression, high quality 3D render"`
    - 差例：`"A city"` （缺运动描述），或 `"Abstract glowing tech nodes"`（太抽象太花里胡哨）
  - visual.duration：建议秒数（填整数 4-8，默认 6）
  - visual.motion：`"slow"` | `"medium"` | `"fast"`
  - visual.fallback：**必须填写**，格式 `"ai_image::英文静态描述, high quality 3D realistic cartoon style"`
  - avatar.mode：**强烈建议 "hidden"**
  - transition：建议 `"crossfade"` 或 `"fade_black"`
  - source 填 null（系统自动设为 assets/videos/{scene_id}.mp4）

## 拆分规则（非常重要！）

1. **细粒度**：旁白超过 15 个字必须拆成两个场景。
2. **节奏感**：ai_video 前后建议用 solid_bg 或 clipart 做缓冲，不要连续出现两个 ai_video。
3. **成本意识**：ai_video ≤ 2 个，ai_image ≤ 3 个，其余尽量免费。

## Avatar 布局规则

- 展示图片 / 播放 ai_video 时：**hidden**。
- 过渡/总结时：**pip_br** 或 **split_right**。
- title_card 和 ai_video 场景必须 **hidden**。

## 需求清单生成规则

- `image`/`clipart`：description 包含精准英文搜索关键词。
- `ai_image`：description 填完整英文 prompt（供 API 生成）。
- `ai_video`：description 填 `[Prompt] 完整英文prompt | Duration: Xs | Motion: slow/medium/fast`（供用户去 AI 视频平台生成）。

## 重要约束

- 只输出 JSON 对象，不要任何解释文字。
- ai_image/ai_video 的 prompt 必须用英文；solid_bg 用精简中文。
- 所有字段必须齐全，不能缺 key（不需要的填 null）。
- ai_video 的 visual.fallback 字段**不能为 null**，必须提供 ai_image 备用方案。"""


# v1 兼容的简单 prompt（不含 avatar）
SYSTEM_PROMPT_V1 = """你是一个视频脚本结构化工具。用户会给你一段视频文案（纯文本），你需要将它拆分成多个场景，输出严格的 JSON 数组。

每个场景的格式：
{
  "id": "01_关键词",
  "text": "旁白文案",
  "visual": {
    "type": "ai_image",
    "prompt": "英文图片描述, high quality 3D realistic cartoon style, 16:9",
    "scene_class": null,
    "source": null,
    "fallback": null
  },
  "audio": {
    "mode": "auto",
    "override": null
  }
}

规则：
1. 按自然段落或语义拆分场景，每段 1-3 句话
2. id 格式：两位数序号_英文关键词，如 01_intro, 02_concept, 03_example
3. visual.type 默认用 "ai_image"，除非文案明显涉及数学公式/图表/代码演示（用 "manim"）
4. visual.prompt 必须用英文，风格统一：高质量3D写实卡通、明亮整洁、16:9。不要太抽象。
5. audio.mode 默认 "auto"
6. 只输出 JSON 数组，不要任何解释文字"""


FREE_ASSET_HINT = (
    "优先使用免费开源素材：OpenMoji / unDraw / Storyset / SVG Repo / "
    "Wikimedia Commons / PublicDomainVectors。"
)


_TOPIC_KEYWORDS = {
    "tech": ("ai", "llm", "model", "algorithm", "software", "chip", "cloud", "prompt", "机器学习", "算法", "模型", "芯片", "软件"),
    "business": ("market", "revenue", "startup", "customer", "sales", "finance", "投资", "商业", "市场", "营收", "公司"),
    "science": ("physics", "chemistry", "biology", "experiment", "hypothesis", "scientific", "物理", "化学", "生物", "实验", "科研"),
    "education": ("lesson", "classroom", "student", "teacher", "curriculum", "学习", "教学", "课堂", "学生", "老师"),
    "health": ("health", "medical", "hospital", "doctor", "disease", "nutrition", "医疗", "健康", "医院", "医生", "营养"),
    "history": ("history", "ancient", "war", "dynasty", "century", "historical", "timeline", "revolution", "历史", "朝代", "战争", "古代", "革命", "时间线"),
    "law": ("law", "legal", "court", "contract", "compliance", "法规", "法律", "合规", "合同", "法院"),
    "lifestyle": ("travel", "food", "fitness", "habit", "family", "旅游", "美食", "健身", "生活", "家庭"),
}

_GENERALIZATION_SUFFIX = """
[GENERALIZATION_RULES]
- The topic can be ANY domain. Do not force AI/LLM examples unless the source text explicitly asks for them.
- Respect the original narration text. You may fix grammar or awkward phrasing to improve spoken fluency, but you MUST NOT rewrite paragraphs, drop sentences, or change the original pacing and factual meaning.
- Visual prompts must be semantically aligned with the scene text, concrete, and strictly use "high quality 3D realistic cartoon style". Do not use abstract or flashy concepts.
- Prefer low-cost assets first: clipart/image/manim/solid_bg. Use ai_image only when truly necessary for key scenes.
- If the script language is Chinese, keep narration text in Chinese. If English, keep English.
"""

_LANGUAGE_RULES = {
    "zh": """
[LANGUAGE_RULES]
- Output narration `text` in Simplified Chinese.
- Keep tone natural spoken Chinese.
- `title_card` visual.prompt should be Chinese first; optional English subtitle is allowed.
""",
    "en": """
[LANGUAGE_RULES]
- Output narration `text` in natural English.
- Keep tone clear and concise for voice-over.
- `title_card` visual.prompt should be English only.
- Do not add Chinese characters unless they are required quoted terms from source text.
""",
}

_CONTENT_BLOCK_RE = re.compile(
    r"『文案正文开始』(?P<body>[\s\S]*?)『文案正文结束』",
    flags=re.IGNORECASE,
)


def _contains_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text or "")


def _is_short_sentence(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return True
    if _contains_cjk(t):
        return len(t) <= 16
    words = [w for w in re.split(r"\s+", t) if w]
    return len(words) <= 9 or len(t) <= 56


def _infer_topic_label(text: str) -> str:
    low = (text or "").lower()
    hit_count: dict[str, int] = {}
    for topic, kws in _TOPIC_KEYWORDS.items():
        count = sum(1 for kw in kws if kw.lower() in low)
        if count > 0:
            hit_count[topic] = count
    if not hit_count:
        return "general"
    return max(hit_count, key=hit_count.get)


def _resolve_target_lang(target_lang: str, normalized_text: str) -> str:
    lang = (target_lang or "auto").strip().lower()
    if lang in ("zh", "zh-cn", "cn", "chinese"):
        return "zh"
    if lang in ("en", "english"):
        return "en"
    return "zh" if _contains_cjk(normalized_text) else "en"


def _build_system_prompt(has_avatar: bool, normalized_text: str, target_lang: str, visual_mode: str = "image") -> str:
    if not has_avatar:
        base = SYSTEM_PROMPT_V1
    elif visual_mode == "video":
        base = SYSTEM_PROMPT_VIDEO
    else:
        base = SYSTEM_PROMPT
    topic = _infer_topic_label(normalized_text)
    lang = _resolve_target_lang(target_lang, normalized_text)
    topic_line = f"[TOPIC_HINT]\nDetected topic: {topic}. Keep visuals and metaphors in this domain.\n"
    lang_line = f"[TARGET_LANGUAGE]\nUse language: {lang}\n"
    lang_rules = _LANGUAGE_RULES.get(lang, "")
    return f"{base}\n\n{topic_line}{lang_line}{_GENERALIZATION_SUFFIX}\n{lang_rules}"


def _extract_content_body(text: str) -> str:
    """
    Extract content between [CONTENT_START] and [CONTENT_END] when present.
    This avoids language/topic auto-detection being polluted by wrapper notes.
    """
    raw = text or ""
    match = _CONTENT_BLOCK_RE.search(raw)
    if not match:
        return raw
    body = (match.group("body") or "").strip()
    return body or raw


def _normalize_input_text(text: str) -> str:
    """把不规范 txt 尽量清洗成稳定输入，降低 LLM 结构化失败概率。"""
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"```[\s\S]*?```", "\n", text)

    cleaned_lines = []
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue

        # Markdown 标题转章节标记，便于生成 title_card
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            if title:
                cleaned_lines.append(f"=== {title} ===")
            continue

        # 仅仅清理多余的空格，保留原本的 Markdown 格式和列表符
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def _clean_scene_text(text: str) -> str:
    text = str(text or "")
    text = text.replace("*", "").replace("`", "")
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _make_scene_id(raw_id: Any, idx: int, used_ids: set[str]) -> str:
    base = str(raw_id or "").strip().lower()
    base = re.sub(r"[^0-9a-zA-Z_]+", "_", base).strip("_")
    if not base:
        base = f"{idx:02d}_scene"
    if not re.match(r"^\d{2}_", base):
        base = f"{idx:02d}_{base}"

    sid = base
    bump = 1
    while sid in used_ids:
        sid = f"{base}_{bump}"
        bump += 1
    used_ids.add(sid)
    return sid


def _looks_formula_scene(text: str) -> bool:
    t = text or ""
    low = t.lower()
    formula_tokens = (
        "公式", "定理", "推导", "矩阵", "函数", "概率", "坐标", "统计", "流程图", "时序图",
        "equation", "theorem", "matrix", "function", "probability", "chart", "timeline",
        "attention", "logit", "token", "derivative", "integral", "regression",
    )
    return "=" in t or any(tok in low for tok in formula_tokens)


def _normalize_scene(raw_scene: Any, idx: int, used_ids: set[str], has_avatar: bool) -> dict:
    scene = raw_scene if isinstance(raw_scene, dict) else {}
    scene_id = _make_scene_id(scene.get("id"), idx, used_ids)
    text = _clean_scene_text(scene.get("text", ""))

    visual_raw = scene.get("visual") if isinstance(scene.get("visual"), dict) else {}
    vtype = str(visual_raw.get("type", "solid_bg")).strip().lower()
    if vtype not in VALID_VISUAL_TYPES:
        vtype = "solid_bg"

    prompt = visual_raw.get("prompt")
    source = visual_raw.get("source")
    scene_class = visual_raw.get("scene_class")
    fallback = visual_raw.get("fallback")
    # ai_video 专有字段
    video_duration = visual_raw.get("duration")
    video_motion = visual_raw.get("motion")

    if vtype == "title_card":
        title_text = _clean_scene_text(prompt or source or text or f"章节 {idx:02d}")
        text = ""
        prompt = title_text
        source = None
        scene_class = None
    elif vtype == "manim":
        if not scene_class:
            scene_class = f"AutoScene{idx:02d}"
        if not prompt and text:
            prompt = f"Create a clear educational manim scene for: {text}"
        source = None
    elif vtype == "ai_image":
        if not prompt and text:
            prompt = (
                f"educational illustration about {text}, high quality 3D "
                f"realistic cartoon style, bright, clean, easy to understand"
            )
        source = None
        scene_class = None
    elif vtype == "ai_video":
        if not source:
            source = f"assets/videos/{scene_id}.mp4"
        if not prompt and text:
            prompt = (
                f"3D realistic cartoon style animation related to: {text}, "
                f"smooth motion, bright, clean, easy to understand"
            )
        scene_class = None
    elif vtype in ("clipart", "image"):
        if not source:
            source = f"assets/manual/{scene_id}.png"
        scene_class = None
    elif vtype == "video":
        if not source:
            source = f"assets/manual/{scene_id}.mp4"
        scene_class = None
    else:  # solid_bg
        if not prompt:
            prompt = (text[:10] + "...") if len(text) > 10 else text
            if not prompt:
                prompt = None
        source = None
        scene_class = None

    avatar_raw = scene.get("avatar") if isinstance(scene.get("avatar"), dict) else {}
    avatar_mode = str(avatar_raw.get("mode", "hidden")).strip().lower()
    if avatar_mode not in VALID_AVATAR_MODES:
        if has_avatar and _is_short_sentence(text):
            avatar_mode = "pip_br"
        else:
            avatar_mode = "hidden"
    try:
        avatar_scale = float(avatar_raw.get("scale", 0.3))
    except (TypeError, ValueError):
        avatar_scale = 0.3
    avatar_scale = max(0.2, min(1.0, avatar_scale))
    if vtype == "title_card":
        avatar_mode = "hidden"

    audio_raw = scene.get("audio") if isinstance(scene.get("audio"), dict) else {}
    audio_mode = str(audio_raw.get("mode", "auto")).strip().lower()
    if audio_mode not in VALID_AUDIO_MODES:
        audio_mode = "auto"
    audio_override = audio_raw.get("override")
    if audio_override is not None and not isinstance(audio_override, str):
        audio_override = None

    transition = str(scene.get("transition", "crossfade")).strip().lower()
    if transition not in VALID_TRANSITIONS:
        transition = "crossfade"

    visual_dict: dict = {
        "type": vtype,
        "prompt": prompt,
        "source": source,
        "scene_class": scene_class,
        "fallback": fallback,
    }
    if vtype == "ai_video":
        # 强制 avatar hidden，保留 duration/motion 供 needs_list 使用
        avatar_mode = "hidden"
        try:
            visual_dict["duration"] = int(video_duration) if video_duration is not None else 6
        except (TypeError, ValueError):
            visual_dict["duration"] = 6
        visual_dict["motion"] = str(video_motion).lower() if video_motion in ("slow", "medium", "fast") else "medium"

    return {
        "id": scene_id,
        "text": text,
        "visual": visual_dict,
        "avatar": {
            "mode": avatar_mode,
            "scale": avatar_scale,
        },
        "audio": {
            "mode": audio_mode,
            "override": audio_override,
        },
        "transition": transition,
    }


def _rebalance_visual_cost(scenes: list[dict], needs_list: list[dict]) -> tuple[list[dict], list[dict], int]:
    """降低 ai_image 比例，优先转为 clipart/solid_bg/manim，减少付费生图依赖。"""
    ai_indices = [i for i, s in enumerate(scenes) if s.get("visual", {}).get("type") == "ai_image"]
    if not ai_indices:
        return scenes, needs_list, 0

    ai_budget = max(1, min(3, len(scenes) // 6 + 1))
    keep: list[int] = []

    # 优先保留开头/结尾和强叙事节点
    for i in ai_indices:
        text = scenes[i].get("text", "")
        low = text.lower()
        if i == 0 or i == len(scenes) - 1 or any(
            k in text or k in low
            for k in ("开场", "核心", "本质", "总结", "结语", "intro", "hook", "core", "summary", "takeaway", "conclusion")
        ):
            keep.append(i)
    for i in ai_indices:
        if len(keep) >= ai_budget:
            break
        if i not in keep:
            keep.append(i)

    keep_set = set(keep[:ai_budget])

    for i in ai_indices:
        if i in keep_set:
            continue
        scene = scenes[i]
        sid = scene["id"]
        text = scene.get("text", "")
        visual = scene.get("visual", {})

        if _looks_formula_scene(text):
            scene["visual"] = {
                "type": "manim",
                "prompt": visual.get("prompt") or f"Show a clean formula animation for: {text}",
                "source": None,
                "scene_class": f"AutoFormula{sid.replace('_', '').title()}",
                "fallback": visual.get("fallback"),
            }
            continue

        # 短句直接用 solid_bg，长句引导到免费插画素材
        if _is_short_sentence(text):
            scene["visual"] = {
                "type": "solid_bg",
                "prompt": visual.get("prompt") or ((text[:10] + "...") if len(text) > 10 else text),
                "source": None,
                "scene_class": None,
                "fallback": visual.get("fallback"),
            }
        else:
            scene["visual"] = {
                "type": "clipart",
                "prompt": visual.get("prompt"),
                "source": f"assets/manual/{sid}.png",
                "scene_class": None,
                "fallback": visual.get("fallback"),
            }
            needs_list.append({
                "scene_id": sid,
                "type": "clipart",
                "filename": f"assets/manual/{sid}.png",
                "description": f"{FREE_ASSET_HINT}（建议与旁白语义一致）",
                "is_optional": False,
            })

    ai_count = sum(1 for s in scenes if s.get("visual", {}).get("type") == "ai_image")
    return scenes, needs_list, ai_count


def _rebalance_ai_video_cost(scenes: list[dict], needs_list: list[dict], visual_mode: str) -> tuple[list[dict], list[dict], int]:
    """
    image 模式：将所有 ai_video 降级为 ai_image（使用 fallback prompt）。
    video 模式：限制 ai_video 总数 ≤ 2，超出部分降级为 ai_image。
    """
    video_indices = [i for i, s in enumerate(scenes) if s.get("visual", {}).get("type") == "ai_video"]
    if not video_indices:
        return scenes, needs_list, 0

    if visual_mode == "video":
        budget = 2
        keep_set = set(video_indices[:budget])
    else:
        keep_set = set()  # image 模式全部降级

    for i in video_indices:
        if i in keep_set:
            continue
        scene = scenes[i]
        visual = scene.get("visual", {})
        # 提取 fallback prompt（格式 "ai_image::实际prompt" 或直接用原 prompt）
        fallback_raw = visual.get("fallback") or ""
        if isinstance(fallback_raw, str) and fallback_raw.startswith("ai_image::"):
            img_prompt = fallback_raw[len("ai_image::"):]
        else:
            img_prompt = (
                visual.get("prompt")
                or f"high quality 3D realistic cartoon style still frame, {scene.get('text', '')}, bright, clean"
            )
        scene["visual"] = {
            "type": "ai_image",
            "prompt": img_prompt,
            "source": None,
            "scene_class": None,
            "fallback": None,
        }

    ai_video_count = sum(1 for s in scenes if s.get("visual", {}).get("type") == "ai_video")
    return scenes, needs_list, ai_video_count


def _build_needs_list(scenes: list[dict], raw_needs: Any) -> tuple[list[dict], int, int]:
    normalized: list[dict] = []
    if isinstance(raw_needs, list):
        for item in raw_needs:
            if not isinstance(item, dict):
                continue
            normalized.append(dict(item))

    for s in scenes:
        sid = s["id"]
        visual = s.get("visual", {})
        vtype = visual.get("type")

        if vtype == "ai_image":
            normalized.append({
                "scene_id": sid,
                "type": "ai_image",
                "filename": f"assets/images/{sid}.png",
                "description": f"[Prompt] {visual.get('prompt')}",
                "is_optional": True,
            })
        elif vtype == "ai_video":
            duration = visual.get("duration", 6)
            motion = visual.get("motion", "medium")
            prompt = visual.get("prompt", "")
            normalized.append({
                "scene_id": sid,
                "type": "ai_video",
                "filename": f"assets/videos/{sid}.mp4",
                "description": f"[Prompt] {prompt} | Duration: {duration}s | Motion: {motion}",
                "prompt": prompt,
                "duration": duration,
                "motion": motion,
                "is_optional": False,
            })
        elif vtype in ("clipart", "image", "video"):
            src = visual.get("source") or ""
            if isinstance(src, str) and src.startswith("assets/manual/"):
                desc = FREE_ASSET_HINT if vtype == "clipart" else "请准备与场景匹配的素材。"
                normalized.append({
                    "scene_id": sid,
                    "type": vtype,
                    "filename": src,
                    "description": desc,
                    "is_optional": False,
                })

    # 去重
    dedup = {}
    for item in normalized:
        scene_id = item.get("scene_id", "")
        itype = item.get("type", "")
        filename = item.get("filename", "")
        key = (scene_id, itype, filename)
        dedup[key] = item

    needs = list(dedup.values())
    ai_image_count = sum(1 for s in scenes if s.get("visual", {}).get("type") == "ai_image")
    ai_video_count = sum(1 for s in scenes if s.get("visual", {}).get("type") == "ai_video")
    return needs, ai_image_count, ai_video_count


def _normalize_scenes(scenes: list[Any], has_avatar: bool) -> list[dict]:
    used_ids: set[str] = set()
    normalized = []
    for i, scene in enumerate(scenes, start=1):
        normalized.append(_normalize_scene(scene, i, used_ids, has_avatar))
    return normalized


def convert_text_to_json(
    text: str,
    output_path: str,
    config_path: str = None,
    has_avatar: bool = False,
    target_lang: str = "auto",
    visual_mode: str = "image",
) -> dict:
    """
    将纯文本脚本转换为 pipeline JSON 格式。

    has_avatar=True 时使用 v2 导演模式（含 avatar 布局 + needs_list）。
    has_avatar=False 时使用 v1 简单模式（向后兼容）。
    target_lang 支持 auto/zh/en。
    visual_mode: "image"（默认，仅静态图）或 "video"（含 ai_video）。

    返回 {"script_path": str, "needs_list": list, "summary": str}
    """
    cfg = load_config(config_path)
    
    # 提取导演指令（如果有）和真正的文案内容
    raw_str = text or ""
    match = _CONTENT_BLOCK_RE.search(raw_str)
    if match:
        prefix = raw_str[:match.start()].strip()
        content_body = match.group("body").strip()
    else:
        prefix = ""
        content_body = raw_str

    # 仅对待切分的文案内容进行深度清洗（去除影响大模型解析的奇怪符号和换行）
    normalized_body = _normalize_input_text(content_body)
    resolved_lang = _resolve_target_lang(target_lang, normalized_body)

    # 重组干净且无害的 Prompt 发送给 LLM
    if prefix:
        final_user_text = f"{prefix}\n\n『文案正文开始』\n{normalized_body}\n『文案正文结束』"
    else:
        final_user_text = normalized_body

    client = OpenAI(
        api_key=cfg.llm.api_key,
        base_url=cfg.llm.base_url,
    )

    prompt = _build_system_prompt(has_avatar, normalized_body, resolved_lang, visual_mode)

    mode_label = f"[mode] visual_mode={visual_mode}" if has_avatar else ""
    print("正在调用 LLM 导演生成脚本..." if has_avatar else "正在调用 LLM 转换脚本格式...")
    print(f"[language] target={resolved_lang}")
    if mode_label:
        print(mode_label)

    # Qwen3 / GLM thinking 系列模型默认开启思维链，需要关闭以避免 content 为空
    extra_kwargs = {}
    model_name = cfg.llm.model or ""
    if "qwen3" in model_name.lower() or "glm" in model_name.lower():
        extra_kwargs["extra_body"] = {"enable_thinking": False}

    response = client.chat.completions.create(
        model=cfg.llm.model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": final_user_text},
        ],
        temperature=0.1,  # 降低温度以减少幻觉
        max_tokens=8192,  # 确保足够空间输出完整 JSON
        **extra_kwargs,
    )

    msg = response.choices[0].message
    raw_content = msg.content or ""

    # content 为空时检查是否为 thinking 模型（reasoning_content 有内容而 content 没有）
    if not raw_content.strip():
        reasoning = getattr(msg, "reasoning_content", None)
        finish_reason = response.choices[0].finish_reason
        print(f"[warn] LLM content 为空 (finish_reason={finish_reason})")
        if reasoning:
            print(f"[warn] reasoning_content 有内容但 content 为空，模型可能仍处于 thinking 模式")
            print(f"[debug] reasoning_content 前 200 字: {reasoning[:200]}")
        print(f"[debug] model={cfg.llm.model}, usage={response.usage}")
        raw = ""
    else:
        raw = raw_content.strip()

    # 兼容处理：某些模式下 <think>...</think> 可能残留在 content 中
    raw = re.sub(r"<think>[\s\S]*?</think>", "", raw, flags=re.IGNORECASE).strip()

    # 提取 JSON（去掉可能的 markdown 代码块）
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        debug_path = os.path.join(os.path.dirname(output_path) or ".", "debug_llm_response.txt")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"\n[Error] LLM 返回的 JSON 格式非法: {e}")
        print(f"原始返回已保存至: {debug_path}")
        print("尝试使用正则修复异常字符（如 '极' 幻觉）...")
        
        # 修复: 去除尾部逗号
        fixed = re.sub(r",\s*([\]}])", r"\1", raw)

        # 修复: 特定字段幻觉 (优先处理，因为它们可能包含被截断的英文)
        fixed = fixed.replace('极速back', 'fallback')
        fixed = fixed.replace('极速urce', 'source')
        fixed = fixed.replace('cross极速de', 'crossfade')
        fixed = fixed.replace('极速de', 'fade') 
        
        # 修复: 0极3 -> 0.3, 极速3 -> 0.3
        fixed = re.sub(r"0?极速?(\d+)", r"0.\1", fixed)
        
        # 修复: 键名幻觉 (移除键名前的中文，如 极速avatar": -> "avatar":)
        fixed = re.sub(r'[\u4e00-\u9fa5]+([a-zA-Z_]+)":', r'"\1":', fixed)
        
        # 修复: 字符串值的幻觉
        fixed = fixed.replace("极速auto", "auto")
        fixed = fixed.replace("cross极速", "crossfade")
        fixed = fixed.replace("cross极fade", "crossfade")
        
        # 修复: 冒号后的极速 (针对 "scale": 极速3 这种没被上面正则捕获的情况)
        fixed = re.sub(r':\s*极速(\d)', r': 0.\1', fixed)
        
        try:
            data = json.loads(fixed)
            print("  -> 修复成功！")
        except json.JSONDecodeError as e2:
            # Create a fixed debug file to help further debugging
            fixed_debug_path = debug_path.replace(".txt", "_fixed.txt")
            with open(fixed_debug_path, "w", encoding="utf-8") as f:
                f.write(fixed)
            raise ValueError(f"无法解析 LLM 输出，即使尝试修复后仍失败: {e2}\n请检查 {fixed_debug_path}")

    if has_avatar:
        # v2 格式: {"scenes": [...], "needs_list": [...], ...}
        if isinstance(data, dict) and "scenes" in data:
            scenes = data["scenes"]
            needs_list = data.get("needs_list", [])
            summary = data.get("summary", "")
        elif isinstance(data, list):
            # 兼容处理：LLM 未按 v2 要求输出外层字典，直接返回了数组
            scenes = data
            needs_list = []
            summary = ""
        else:
            # LLM 可能输出了单个场景的对象，包装一下
            scenes = [data] if isinstance(data, dict) else []
            needs_list = []
            summary = ""
    else:
        # v1 格式: 直接是数组
        if isinstance(data, list):
            scenes = data
        elif isinstance(data, dict) and "scenes" in data:
            scenes = data["scenes"]
        else:
            raise ValueError("LLM 输出格式无效")
        needs_list = []
        summary = ""

    if not isinstance(scenes, list) or len(scenes) == 0:
        print(f"\n[Raw LLM Output for Debugging]:\n{raw}\n")
        raise ValueError("LLM 输出的 scenes 为空")

    scenes = _normalize_scenes(scenes, has_avatar=has_avatar)

    if has_avatar:
        needs_list, _, _ = _build_needs_list(scenes, needs_list)
        scenes, needs_list, ai_count = _rebalance_visual_cost(scenes, needs_list)
        scenes, needs_list, ai_video_count = _rebalance_ai_video_cost(scenes, needs_list, visual_mode)
        needs_list, ai_count, ai_video_count = _build_needs_list(scenes, needs_list)
        required_count = sum(1 for x in needs_list if not x.get("is_optional", False))
        if visual_mode == "video":
            summary = f"共{len(scenes)}个场景，AI视频{ai_video_count}个，AI生图{ai_count}张，需要你准备{required_count}项素材"
        else:
            summary = f"共{len(scenes)}个场景，需要AI生图{ai_count}张，需要你准备{required_count}项素材"
    else:
        ai_count = sum(1 for s in scenes if s.get("visual", {}).get("type") == "ai_image")
        ai_video_count = 0

    # 写入文件（只写 scenes 数组，pipeline 直接读取）
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)

    print(f"\n已生成 {len(scenes)} 个场景 → {output_path}")

    if has_avatar:
        print(f"AI 生图数量: {ai_count}  |  AI 视频数量: {ai_video_count}")

        if needs_list:
            print(f"\n{'='*50}")
            print("[需求清单] 请准备以下素材：")
            print(f"{'='*50}")
            for item in needs_list:
                itype = item.get("type", "image")
                if itype in ("title_card", "solid_bg", "manim"):
                    continue

                sid = item.get("scene_id", "?")
                desc = item.get("description", "")

                if itype == "ai_image":
                    fname = item.get("filename", f"assets/images/{sid}.png")
                elif itype == "ai_video":
                    fname = item.get("filename", f"assets/videos/{sid}.mp4")
                else:
                    fname = item.get("filename", f"assets/manual/{sid}.png")

                item["filename"] = fname
                tag = "[AI视频]" if itype == "ai_video" else f"[{itype}]"
                print(f"  {tag} [{sid}] {fname}")
                print(f"         {desc}")
            print(f"{'='*50}")
            print("准备好后放入对应路径即可。")
        if summary:
            print(f"\n[统计] {summary}")

        # 同时保存需求清单到独立文件
        if needs_list:
            needs_path = output_path.replace(".json", "_needs.json")
            with open(needs_path, "w", encoding="utf-8") as f:
                json.dump({
                    "needs_list": needs_list,
                    "summary": summary,
                    "ai_image_count": ai_count,
                    "ai_video_count": ai_video_count,
                    "visual_mode": visual_mode,
                }, f, ensure_ascii=False, indent=2)
            print(f"\n需求清单已保存 → {needs_path}")

    return {
        "script_path": output_path,
        "needs_list": needs_list,
        "summary": summary,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="文案 → JSON 转换器（v2 导演模式）")
    parser.add_argument("input", help="输入文件路径（纯文本 .txt）")
    parser.add_argument("-o", "--output", help="输出 JSON 路径", default=None)
    parser.add_argument("--config", help="配置文件路径", default=None)
    parser.add_argument("--avatar", action="store_true", help="启用 v2 导演模式（含 Avatar 布局）")
    parser.add_argument("--lang", default="auto", choices=["auto", "zh", "en"], help="输出脚本语言: auto/zh/en")

    args = parser.parse_args()

    # 读取文案
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    # 默认输出路径：同名 .json
    if args.output is None:
        base = os.path.splitext(args.input)[0]
        args.output = base + ".json"
        if "scripts" not in args.output:
            name = os.path.basename(args.output)
            args.output = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "scripts", name,
            )

    convert_text_to_json(text, args.output, args.config, has_avatar=args.avatar, target_lang=args.lang)
