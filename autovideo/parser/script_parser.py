"""脚本解析器 - 将 script.json 转为结构化 SceneItem 列表"""

import json
import os
from dataclasses import dataclass
from typing import List, Optional


VALID_VISUAL_TYPES = {"manim", "ai_image", "ai_video", "image", "video", "solid_bg", "clipart", "title_card"}
VALID_AUDIO_MODES = {"auto", "manual", "avatar"}
VALID_AVATAR_MODES = {"pip_br", "pip_bl", "pip_tr", "pip_tl", "fullscreen", "split_left", "split_right", "hidden"}
VALID_TRANSITIONS = {"crossfade", "fade_black", "cut"}


@dataclass
class SceneItem:
    id: str
    text: str
    # 视觉
    visual_type: str                     # manim / ai_image / image / video / solid_bg / clipart
    visual_source: Optional[str] = None  # scene_class / prompt / 文件路径
    visual_prompt: Optional[str] = None  # 额外 prompt（主要用于 manim 自动生成）
    visual_fallback: Optional[str] = None
    visual_color: Optional[str] = None   # 主题色（hex，仅 solid_bg 使用，如 "#0d1b2a"）
    # 音频
    audio_mode: str = "auto"             # auto / manual / avatar
    audio_override: Optional[str] = None # 手动指定音频路径（最高优先级）
    # Avatar
    avatar_mode: str = "hidden"          # pip_br / pip_bl / fullscreen / hidden 等
    avatar_scale: float = 0.3            # 画中画缩放比例
    # 转场
    transition: str = "crossfade"        # crossfade / fade_black / cut


def parse_script(script_path: str) -> List[SceneItem]:
    """解析 script.json，返回 SceneItem 列表"""
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"脚本文件不存在: {script_path}")

    # 相对路径校验以脚本文件所在目录为基准（项目目录）
    script_base_dir = os.path.dirname(os.path.abspath(script_path))

    with open(script_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, list):
        raise ValueError("script.json 顶层必须是数组")

    scenes = []
    for i, item in enumerate(raw):
        # 校验必填字段
        for key in ("id", "text", "visual"):
            if key not in item:
                raise ValueError(f"Scene #{i} 缺少必填字段: {key}")

        visual = item["visual"]
        vtype = visual.get("type", "image")
        if vtype not in VALID_VISUAL_TYPES:
            raise ValueError(f"Scene '{item['id']}': visual.type 无效: {vtype}，可选: {VALID_VISUAL_TYPES}")

        # 根据类型提取 source
        if vtype == "manim":
            source = visual.get("scene_class")
            visual_prompt = visual.get("prompt")
        elif vtype in ("ai_image", "solid_bg", "title_card"):
            source = visual.get("prompt") or visual.get("source")
            visual_prompt = visual.get("prompt")
        elif vtype == "ai_video":
            source = visual.get("source") or f"assets/videos/{item['id']}.mp4"
            visual_prompt = visual.get("prompt")
        else:
            source = visual.get("source")
            visual_prompt = visual.get("prompt")

        # solid_bg 主题色（可选，hex 格式）
        visual_color = visual.get("color") if vtype == "solid_bg" else None

        audio = item.get("audio", {})
        audio_mode = audio.get("mode", "auto")
        if audio_mode not in VALID_AUDIO_MODES:
            raise ValueError(f"Scene '{item['id']}': audio.mode 无效: {audio_mode}")

        # Avatar 字段（v2，向后兼容：缺省 hidden）
        avatar = item.get("avatar", {})
        avatar_mode = avatar.get("mode", "hidden")
        if avatar_mode not in VALID_AVATAR_MODES:
            print(f"[warn] Scene '{item['id']}': avatar.mode 无效: {avatar_mode}，使用 hidden")
            avatar_mode = "hidden"
        avatar_scale = avatar.get("scale", 0.3)

        # 转场字段（v2，缺省 crossfade）
        transition = item.get("transition", "crossfade")
        if transition not in VALID_TRANSITIONS:
            transition = "crossfade"

        scene = SceneItem(
            id=item["id"],
            text=item["text"],
            visual_type=vtype,
            visual_source=source,
            visual_prompt=visual_prompt,
            visual_fallback=visual.get("fallback"),
            visual_color=visual_color,
            audio_mode=audio_mode,
            audio_override=audio.get("override"),
            avatar_mode=avatar_mode,
            avatar_scale=avatar_scale,
            transition=transition,
        )
        scenes.append(scene)

    # 校验手动素材是否存在
    for scene in scenes:
        if scene.audio_mode == "manual" and scene.audio_override:
            audio_check = (
                scene.audio_override
                if os.path.isabs(scene.audio_override)
                else os.path.join(script_base_dir, scene.audio_override)
            )
            if not os.path.exists(audio_check):
                print(f"[warn] Scene '{scene.id}': 手动音频文件不存在: {scene.audio_override}")

        if scene.visual_type in ("image", "video", "ai_video") and scene.visual_source:
            check_path = (
                scene.visual_source
                if os.path.isabs(scene.visual_source)
                else os.path.join(script_base_dir, scene.visual_source)
            )
            if not os.path.exists(check_path):
                print(f"[warn] Scene '{scene.id}': 视觉素材不存在: {scene.visual_source}")

    return scenes


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "scripts/example_llm.json"
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base, path)
    scenes = parse_script(full_path)
    for s in scenes:
        print(f"  [{s.id}] type={s.visual_type} audio={s.audio_mode}")
    print(f"\n共 {len(scenes)} 个场景")
