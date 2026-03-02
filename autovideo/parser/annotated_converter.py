"""
带标注的文案转换器 - 支持 [图片] 和 {特效} 标注

用法：
    python -m parser.annotated_converter input.txt -o output.json --avatar

标注语法：
    [xxx.png]       → 用户自备图片，映射为 image 类型
    [xxx.mp4]       → 用户自备视频，映射为 video 类型
    {特效：描述}    → 特效标注，存入 visual.effect 字段
    【画面】...     → 画面描述段落（不朗读）
    【配音】...     → 配音文本段落（TTS 朗读）

详细文档：参见 ANNOTATION_GUIDE.md
"""

import json
import os
import re
import sys
from typing import Any, Optional

from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import load_config
from parser.script_parser import (
    VALID_AUDIO_MODES,
    VALID_AVATAR_MODES,
    VALID_TRANSITIONS,
    VALID_VISUAL_TYPES,
)

# ═══════════════════════════════════════════════════════════════════
#  正则匹配用户标注
# ═══════════════════════════════════════════════════════════════════

# 图片/视频标注 [xxx.png] [xxx.mp4]
_USER_MEDIA_RE = re.compile(
    r'\[([^\[\]]+\.(?:png|jpg|jpeg|gif|webp|mp4|mov|avi))\]',
    re.IGNORECASE
)

# 特效标注 {特效：xxx} 或 {特效:xxx}
_USER_EFFECT_RE = re.compile(r'\{特效[：:]([^}]+)\}')

# 画面段落 【画面】...【/画面】 或 【画面】...【配音】
_VISUAL_BLOCK_RE = re.compile(
    r'【画面】([\s\S]*?)(?:【/画面】|【配音】|(?=【画面】)|$)',
    re.IGNORECASE
)

# 配音段落 【配音】...
_VOICE_BLOCK_RE = re.compile(
    r'【配音(?:/口播)?】([\s\S]*?)(?=【画面】|【配音】|===|$)',
    re.IGNORECASE
)

# 视频扩展名
_VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.webm', '.mkv'}


# ═══════════════════════════════════════════════════════════════════
#  LLM 系统提示词（带标注保留规则）
# ═══════════════════════════════════════════════════════════════════

SYSTEM_PROMPT_ANNOTATED = """你是一个专业视频导演 AI。用户会给你一段带标注的视频文案，你需要：
1. **文案润色**：修复语法、去除 Markdown 格式、让口语更通顺，但**绝对保持核心意思不变**
2. 拆分成多个场景（细粒度，每场景旁白 ≤15 个字）
3. 为每个场景选择最合适的视觉策略和 Avatar 布局
4. **严格保留用户标注**（见下方规则）

## 用户标注保留规则（最高优先级！！！）

当文案中出现以下标注时，**必须原样保留**：

### 1. 图片/视频标注 `[文件名.扩展名]`
- 格式：`[cyber_cat.png]`、`[demo.mp4]`
- **必须**设为用户自备素材：
  - 图片扩展名 (.png/.jpg/.jpeg/.gif/.webp) → `visual.type = "image"`
  - 视频扩展名 (.mp4/.mov/.avi) → `visual.type = "video"`
  - `visual.source = "assets/manual/文件名.xxx"`
- **禁止**用 ai_image 替换！

### 2. 特效标注 `{特效：描述}`
- 格式：`{特效：光效闪烁}` 或 `{特效:粒子效果}`
- 存入 `visual.effect` 字段
- 这是用户想要的视觉效果，必须保留

### 3. 【画面】段落
- 【画面】到【/画面】或【配音】之间的内容是**画面描述**
- 画面描述场景的 `text` 字段应留空 `""`（不朗读）
- 根据画面描述为场景选择 visual 类型（优先使用用户标注的素材）

### 4. 【配音】段落
- 【配音】或【配音/口播】后的内容是**配音文本**
- 需要拆分成多个场景，每场景 ≤15 个字
- `text` 字段填入配音内容

## 输出格式（严格 JSON）

```json
{
  "scenes": [
    {
      "id": "01_intro",
      "text": "配音文案（画面场景留空）",
      "visual": {
        "type": "image | video | solid_bg | clipart | ai_image | manim | title_card",
        "prompt": "英文画面描述（ai_image 用）或中文关键词（solid_bg 用）",
        "source": "assets/manual/xxx.png（用户标注时必填）",
        "effect": "用户标注的特效描述（如有）",
        "scene_class": null,
        "fallback": null
      },
      "avatar": {
        "mode": "pip_br | pip_bl | pip_tr | pip_tl | hidden | split_left | split_right",
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
    {"scene_id": "02_demo", "type": "image", "filename": "assets/manual/demo.png", "description": "用户自备素材"}
  ],
  "summary": "共N个场景，用户素材X个，AI生图Y张"
}
```

## 视觉策略选择规则

1. **title_card**：遇到 `=== 标题 ===` 时使用
2. **image/video**：有用户标注 `[xxx.png/mp4]` 时**必须使用**
3. **solid_bg**：短句过渡、总结、无标注的配音场景
4. **ai_image**：仅用于无用户标注的关键场景（每视频 ≤3 张）
5. **clipart/manim**：根据内容适当使用

## Avatar 布局规则

- 有用户图片/视频的场景：**hidden**（让用户看素材）
- 配音过渡场景：**pip_br** 或 **split_right**
- title_card 场景：**hidden**

## 重要

- 只输出 JSON 对象
- 用户标注的素材**绝对不能**被替换为 ai_image
- visual.effect 字段必须保留用户的特效描述
- 输出字段必须齐全，不能缺 key"""


# ═══════════════════════════════════════════════════════════════════
#  预处理：提取用户标注
# ═══════════════════════════════════════════════════════════════════

def extract_annotations(text: str) -> dict:
    """
    提取文案中的用户标注。

    Returns:
        {
            "media": [{"filename": "xxx.png", "type": "image"}, ...],
            "effects": ["光效闪烁", ...],
            "visual_blocks": ["画面描述1", ...],
            "voice_blocks": ["配音文本1", ...]
        }
    """
    annotations = {
        "media": [],
        "effects": [],
        "visual_blocks": [],
        "voice_blocks": [],
    }

    # 提取图片/视频标注
    seen_media = set()
    for match in _USER_MEDIA_RE.finditer(text):
        filename = match.group(1)
        if filename not in seen_media:
            seen_media.add(filename)
            ext = os.path.splitext(filename)[1].lower()
            media_type = "video" if ext in _VIDEO_EXTENSIONS else "image"
            annotations["media"].append({
                "filename": filename,
                "type": media_type,
                "source": f"assets/manual/{filename}",
            })

    # 提取特效标注
    for match in _USER_EFFECT_RE.finditer(text):
        effect_desc = match.group(1).strip()
        if effect_desc:
            annotations["effects"].append(effect_desc)

    # 提取画面段落
    for match in _VISUAL_BLOCK_RE.finditer(text):
        block = match.group(1).strip()
        if block:
            annotations["visual_blocks"].append(block)

    # 提取配音段落
    for match in _VOICE_BLOCK_RE.finditer(text):
        block = match.group(1).strip()
        if block:
            annotations["voice_blocks"].append(block)

    return annotations


def _normalize_input_text(text: str) -> str:
    """清洗输入文本，但保留用户标注。"""
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 保留用户标注，只清理多余空白
    cleaned_lines = []
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue

        # Markdown 标题转章节标记
        if line.startswith("#") and not line.startswith("##"):
            title = line.lstrip("#").strip()
            if title:
                cleaned_lines.append(f"=== {title} ===")
            continue

        # 保留标注符号 [] {} 【】
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# ═══════════════════════════════════════════════════════════════════
#  后处理：规范化场景数据
# ═══════════════════════════════════════════════════════════════════

def _clean_scene_text(text: str) -> str:
    """清理场景文本。"""
    text = str(text or "")
    text = text.replace("*", "").replace("`", "")
    text = re.sub(r"#+\s*", "", text)
    # 移除标注符号（已被提取）
    text = _USER_MEDIA_RE.sub("", text)
    text = _USER_EFFECT_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _make_scene_id(raw_id: Any, idx: int, used_ids: set) -> str:
    """生成唯一的场景 ID。"""
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


def _is_short_sentence(text: str) -> bool:
    """判断是否为短句。"""
    t = (text or "").strip()
    if not t:
        return True
    # 中文按字符计数
    if any("\u4e00" <= ch <= "\u9fff" for ch in t):
        return len(t) <= 16
    # 英文按单词计数
    words = [w for w in re.split(r"\s+", t) if w]
    return len(words) <= 9 or len(t) <= 56


def _normalize_scene(raw_scene: Any, idx: int, used_ids: set, has_avatar: bool) -> dict:
    """规范化单个场景数据。"""
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
    effect = visual_raw.get("effect")  # 保留特效标注

    # 处理各种 visual 类型
    if vtype == "title_card":
        title_text = _clean_scene_text(prompt or source or text or f"章节 {idx:02d}")
        text = ""
        prompt = title_text
        source = None
        scene_class = None
    elif vtype in ("image", "video"):
        # 用户素材，保持 source 不变
        if not source:
            source = f"assets/manual/{scene_id}.{'mp4' if vtype == 'video' else 'png'}"
        scene_class = None
    elif vtype == "ai_image":
        if not prompt and text:
            prompt = f"educational illustration about {text}, digital art, cinematic lighting, 4k"
        source = None
        scene_class = None
    elif vtype == "manim":
        if not scene_class:
            scene_class = f"AutoScene{idx:02d}"
        if not prompt and text:
            prompt = f"Create a clear educational manim scene for: {text}"
        source = None
    elif vtype in ("clipart",):
        if not source:
            source = f"assets/manual/{scene_id}.png"
        scene_class = None
    else:  # solid_bg
        if not prompt:
            prompt = (text[:10] + "...") if len(text) > 10 else text
            if not prompt:
                prompt = None
        source = None
        scene_class = None

    # Avatar 布局
    avatar_raw = scene.get("avatar") if isinstance(scene.get("avatar"), dict) else {}
    avatar_mode = str(avatar_raw.get("mode", "hidden")).strip().lower()
    if avatar_mode not in VALID_AVATAR_MODES:
        if has_avatar and _is_short_sentence(text) and vtype not in ("image", "video", "title_card"):
            avatar_mode = "pip_br"
        else:
            avatar_mode = "hidden"
    try:
        avatar_scale = float(avatar_raw.get("scale", 0.3))
    except (TypeError, ValueError):
        avatar_scale = 0.3
    avatar_scale = max(0.2, min(1.0, avatar_scale))

    # 用户素材场景强制隐藏 avatar
    if vtype in ("image", "video", "title_card"):
        avatar_mode = "hidden"

    # Audio
    audio_raw = scene.get("audio") if isinstance(scene.get("audio"), dict) else {}
    audio_mode = str(audio_raw.get("mode", "auto")).strip().lower()
    if audio_mode not in VALID_AUDIO_MODES:
        audio_mode = "auto"
    audio_override = audio_raw.get("override")

    # Transition
    transition = str(scene.get("transition", "crossfade")).strip().lower()
    if transition not in VALID_TRANSITIONS:
        transition = "crossfade"

    visual_dict = {
        "type": vtype,
        "prompt": prompt,
        "source": source,
        "scene_class": scene_class,
        "fallback": fallback,
    }
    # 保留特效字段（如果有）
    if effect:
        visual_dict["effect"] = effect

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


def _normalize_scenes(scenes: list, has_avatar: bool) -> list:
    """规范化所有场景。"""
    used_ids: set = set()
    normalized = []
    for i, scene in enumerate(scenes, start=1):
        normalized.append(_normalize_scene(scene, i, used_ids, has_avatar))
    return normalized


def _build_needs_list(scenes: list, user_media: list) -> tuple:
    """构建需求清单。"""
    needs_list = []
    seen = set()

    # 添加用户标注的素材
    for media in user_media:
        key = (media["filename"], media["type"])
        if key not in seen:
            seen.add(key)
            needs_list.append({
                "scene_id": "user_annotated",
                "type": media["type"],
                "filename": media["source"],
                "description": "用户自备素材（已在文案中标注）",
                "is_optional": False,
            })

    # 添加需要 AI 生成的图片
    ai_image_count = 0
    for scene in scenes:
        visual = scene.get("visual", {})
        vtype = visual.get("type")
        sid = scene["id"]

        if vtype == "ai_image":
            ai_image_count += 1
            needs_list.append({
                "scene_id": sid,
                "type": "ai_image",
                "filename": f"assets/images/{sid}.png",
                "description": f"[Prompt] {visual.get('prompt', '')}",
                "is_optional": True,
            })

    user_media_count = len(user_media)
    return needs_list, user_media_count, ai_image_count


# ═══════════════════════════════════════════════════════════════════
#  主转换函数
# ═══════════════════════════════════════════════════════════════════

def convert_annotated_text(
    text: str,
    output_path: str,
    config_path: str = None,
    has_avatar: bool = True,
    target_lang: str = "zh",
) -> dict:
    """
    将带标注的文案转换为 pipeline JSON 格式。

    Args:
        text: 输入文案（带标注）
        output_path: 输出 JSON 路径
        config_path: 配置文件路径
        has_avatar: 是否启用 Avatar
        target_lang: 目标语言

    Returns:
        {"script_path": str, "needs_list": list, "summary": str, "annotations": dict}
    """
    cfg = load_config(config_path)

    # 1. 提取用户标注
    annotations = extract_annotations(text)
    print(f"\n[标注提取]")
    print(f"  图片/视频: {len(annotations['media'])} 个")
    print(f"  特效标注: {len(annotations['effects'])} 个")
    print(f"  画面段落: {len(annotations['visual_blocks'])} 个")
    print(f"  配音段落: {len(annotations['voice_blocks'])} 个")

    if annotations["media"]:
        print(f"\n  用户素材:")
        for m in annotations["media"]:
            print(f"    [{m['type']}] {m['filename']} → {m['source']}")

    # 2. 清洗文本
    normalized_text = _normalize_input_text(text)

    # 3. 调用 LLM
    client = OpenAI(
        api_key=cfg.llm.api_key,
        base_url=cfg.llm.base_url,
    )

    print(f"\n[LLM] 正在调用 {cfg.llm.model} 生成脚本...")

    # 构建 LLM 请求
    extra_kwargs = {}
    model_name = cfg.llm.model or ""
    if "qwen3" in model_name.lower() or "glm" in model_name.lower():
        extra_kwargs["extra_body"] = {"enable_thinking": False}

    response = client.chat.completions.create(
        model=cfg.llm.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_ANNOTATED},
            {"role": "user", "content": normalized_text},
        ],
        temperature=0.1,
        max_tokens=8192,
        **extra_kwargs,
    )

    raw_content = response.choices[0].message.content or ""
    raw = raw_content.strip()

    # 处理 thinking 模式残留
    raw = re.sub(r"<think>[\s\S]*?</think>", "", raw, flags=re.IGNORECASE).strip()

    # 提取 JSON
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        debug_path = os.path.join(os.path.dirname(output_path) or ".", "debug_annotated_response.txt")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"\n[Error] LLM 返回的 JSON 格式非法: {e}")
        print(f"原始返回已保存至: {debug_path}")
        raise ValueError(f"无法解析 LLM 输出: {e}")

    # 4. 提取场景
    if isinstance(data, dict) and "scenes" in data:
        scenes = data["scenes"]
        raw_needs = data.get("needs_list", [])
        summary = data.get("summary", "")
    elif isinstance(data, list):
        scenes = data
        raw_needs = []
        summary = ""
    else:
        scenes = [data] if isinstance(data, dict) else []
        raw_needs = []
        summary = ""

    if not scenes:
        raise ValueError("LLM 输出的 scenes 为空")

    # 5. 规范化场景
    scenes = _normalize_scenes(scenes, has_avatar=has_avatar)

    # 6. 验证用户标注是否被保留
    user_sources = {m["source"] for m in annotations["media"]}
    preserved_sources = set()
    for scene in scenes:
        source = scene.get("visual", {}).get("source")
        if source and source in user_sources:
            preserved_sources.add(source)

    if user_sources:
        missing = user_sources - preserved_sources
        if missing:
            print(f"\n[警告] 以下用户标注未被保留（可能被 LLM 忽略）:")
            for m in missing:
                print(f"  - {m}")
        else:
            print(f"\n[OK] 所有用户标注已保留")

    # 7. 构建需求清单
    needs_list, user_count, ai_count = _build_needs_list(scenes, annotations["media"])
    summary = f"共{len(scenes)}个场景，用户素材{user_count}个，AI生图{ai_count}张"

    # 8. 写入文件
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)

    print(f"\n[输出] {len(scenes)} 个场景 → {output_path}")
    print(f"[统计] {summary}")

    # 保存需求清单
    if needs_list:
        needs_path = output_path.replace(".json", "_needs.json")
        with open(needs_path, "w", encoding="utf-8") as f:
            json.dump({
                "needs_list": needs_list,
                "summary": summary,
                "user_media_count": user_count,
                "ai_image_count": ai_count,
                "annotations": annotations,
            }, f, ensure_ascii=False, indent=2)
        print(f"[需求清单] → {needs_path}")

    return {
        "script_path": output_path,
        "needs_list": needs_list,
        "summary": summary,
        "annotations": annotations,
    }


# ═══════════════════════════════════════════════════════════════════
#  命令行入口
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="带标注的文案转换器 - 支持 [图片] 和 {特效} 标注",
        epilog="详细文档：参见 parser/ANNOTATION_GUIDE.md"
    )
    parser.add_argument("input", help="输入文件路径（带标注的 .txt）")
    parser.add_argument("-o", "--output", help="输出 JSON 路径", default=None)
    parser.add_argument("--config", help="配置文件路径", default=None)
    parser.add_argument("--avatar", action="store_true", help="启用 Avatar 模式", default=True)
    parser.add_argument("--lang", default="zh", choices=["zh", "en"], help="输出脚本语言")

    args = parser.parse_args()

    # 读取文案
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    # 默认输出路径
    if args.output is None:
        base = os.path.splitext(args.input)[0]
        args.output = base + ".json"

    result = convert_annotated_text(
        text,
        args.output,
        config_path=args.config,
        has_avatar=args.avatar,
        target_lang=args.lang,
    )

    print(f"\n{'='*50}")
    print("转换完成！")
    print(f"{'='*50}")
    print(f"脚本: {result['script_path']}")
    print(f"统计: {result['summary']}")

    if result["annotations"]["media"]:
        print(f"\n请确保以下素材已放入 assets/manual/ 目录:")
        for m in result["annotations"]["media"]:
            print(f"  - {m['filename']}")
