"""
字幕和标题渲染测试脚本
用法: python test_subtitle.py
读取 config.yaml 的设置，生成测试视频验证效果
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from config import load_config
from compositor.assembler import _make_subtitle_clip, _resolve_visual, _make_gradient_bg
from parser.script_parser import SceneItem
import numpy as np
from moviepy import ColorClip, CompositeVideoClip, concatenate_videoclips

# 读取配置
cfg = load_config()
WIDTH  = cfg.video.width
HEIGHT = cfg.video.height
FPS    = cfg.video.fps
SUB_FONT      = cfg.subtitle.font
SUB_FS        = cfg.subtitle.font_size
TITLE_FS      = cfg.subtitle.title_font_size
SUB_COLOR     = cfg.subtitle.color
AVATAR_MODE   = cfg.avatar.default_mode
AVATAR_MARGIN = cfg.avatar.margin

# split_left 内容区
AVATAR_W   = int(WIDTH * 0.35)
CONTENT_X  = AVATAR_W if AVATAR_MODE == "split_left" else 0
CONTENT_W  = WIDTH - AVATAR_W if AVATAR_MODE.startswith("split_") else WIDTH

print(f"config: {WIDTH}x{HEIGHT}  font_size={SUB_FS}  title_font_size={TITLE_FS}")
print(f"avatar_mode={AVATAR_MODE}  content_x={CONTENT_X}  content_w={CONTENT_W}")
print()


def generate_test_video():
    clips = []

    # ── 场景1: solid_bg 标题卡 ──────────────────────────
    print("[1/3] 标题卡 (solid_bg)...")
    scene_title = SceneItem(
        id="test_solid_bg",
        text="",
        visual_type="solid_bg",
        visual_source="视觉模型与多模态",
        visual_fallback=None,
        audio_mode="auto",
        audio_override=None,
        avatar_mode="hidden",
        avatar_scale=1.0,
        transition="crossfade",
    )
    clip1 = _resolve_visual(scene_title, BASE_DIR, 2.0, (WIDTH, HEIGHT),
                            title_font_size=TITLE_FS)
    if clip1 is None:
        clip1 = _make_gradient_bg(WIDTH, HEIGHT, 2.0)
    clips.append(clip1)

    # ── 场景2: split_left 字幕（短文本）────────────────────
    print("[2/3] split_left 字幕（短文本）...")
    bg2 = _make_gradient_bg(WIDTH, HEIGHT, 3.0)

    # 左侧 avatar 区（灰色方块模拟）
    avatar_block = ColorClip(size=(AVATAR_W, HEIGHT), color=(80, 80, 100), duration=3.0)
    split_bg = CompositeVideoClip([
        bg2,
        avatar_block.with_position((0, 0)),
    ], size=(WIDTH, HEIGHT))

    sub2 = _make_subtitle_clip(
        text="要理解AI的眼睛，就不得不提和NLP。",
        duration=3.0,
        width=WIDTH,
        height=HEIGHT,
        font=SUB_FONT,
        font_size=SUB_FS,
        color=SUB_COLOR,
        content_x=CONTENT_X,
        content_w=CONTENT_W,
    )
    scene2 = CompositeVideoClip([split_bg, sub2], size=(WIDTH, HEIGHT)) if sub2 else split_bg
    clips.append(scene2)

    # ── 场景3: split_left 字幕（长文本，测试换行）──────────
    print("[3/3] split_left 字幕（长文本，测试换行）...")
    bg3 = _make_gradient_bg(WIDTH, HEIGHT, 4.0)
    avatar_block3 = ColorClip(size=(AVATAR_W, HEIGHT), color=(80, 80, 100), duration=4.0)
    split_bg3 = CompositeVideoClip([
        bg3,
        avatar_block3.with_position((0, 0)),
    ], size=(WIDTH, HEIGHT))

    sub3 = _make_subtitle_clip(
        text="不管是你每天用的ChatGPT包——它们本质都是LLM，也就是大语言模型。",
        duration=4.0,
        width=WIDTH,
        height=HEIGHT,
        font=SUB_FONT,
        font_size=SUB_FS,
        color=SUB_COLOR,
        content_x=CONTENT_X,
        content_w=CONTENT_W,
    )
    scene3 = CompositeVideoClip([split_bg3, sub3], size=(WIDTH, HEIGHT)) if sub3 else split_bg3
    clips.append(scene3)

    # ── 合成输出 ────────────────────────────────────────
    print("合成中...")
    final = concatenate_videoclips(clips, method="compose")
    out = os.path.join(BASE_DIR, "output", "test_subtitle.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    final.write_videofile(out, fps=FPS, codec="libx264", logger=None)
    print(f"\n[OK] 输出: {out}")
    return out


if __name__ == "__main__":
    generate_test_video()
