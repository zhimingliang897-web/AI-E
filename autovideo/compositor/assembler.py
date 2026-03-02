"""视频合成器 v2.4 - 支持 Avatar 叠加、字幕烧入、渐变背景、转场
修复：
  - 标题偏右/偏移 → TextClip 内部 text_align="center"，外部也居中
  - 字幕底部被截断 → 高度 None 自适应，超高时自动缩字号
  - 描边重影 → stroke_width=1 + 半透明底条
  - 字号不适配 → 所有字号按分辨率缩放（1080p 基准）
"""

import gc
import os
import subprocess
from typing import List, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoClip,
    VideoFileClip,
    concatenate_audioclips,
    concatenate_videoclips,
    vfx,
)
from moviepy.audio.AudioClip import AudioArrayClip

from parser.script_parser import SceneItem


# ===== MoviePy Bug 修复：ColorClip int64 内存溢出 =====
# MoviePy 内部 CompositeVideoClip 创建背景 ColorClip 时，对 color tuple 调用
# np.tile(color, w*h) 会保留 Python int 的默认 int64 dtype，导致每帧分配
# 63 MiB（正常应为 6 MiB uint8）。48 场景累积后内存耗尽。
# 修复：给 ColorClip.__init__ 打补丁，强制将 color 转为 uint8 数组。
import moviepy.video.VideoClip as _mvc
_orig_color_clip_init = _mvc.ColorClip.__init__

def _patched_color_clip_init(self, size, color=None, **kwargs):
    # 只对 tuple/list（RGB 颜色）做 uint8 转换，避免 int64 内存溢出。
    # 标量颜色（mask 用 1.0）不转换，否则 np.array(1.0, dtype=uint8) 变成
    # 0-d 数组，MoviePy with_mask() 的 isinstance 检查会失败。
    if color is not None and isinstance(color, (list, tuple)):
        color = np.array(color, dtype=np.uint8)
    _orig_color_clip_init(self, size, color=color, **kwargs)

_mvc.ColorClip.__init__ = _patched_color_clip_init

import moviepy.video.compositing.CompositeVideoClip as _mp_cvc
_orig_composite_frame_func = _mp_cvc.CompositeVideoClip.frame_function

def _patched_composite_frame_func(self, t):
    if not self.is_mask and getattr(self, "bg", None) is None:
        size = getattr(self, "size", (1920, 1080))
        color = getattr(self, "bg_color", (0, 0, 0))
        if color is None: color = (0, 0, 0)
        self.bg = _mvc.ColorClip(size, color=color, is_mask=self.is_mask)
        self.bg.start = getattr(self, "start", 0)
    return _orig_composite_frame_func(self, t)

_mp_cvc.CompositeVideoClip.frame_function = _patched_composite_frame_func
# ===== 修复结束 =====

# ===== 工具函数 =====

def _check_nvenc() -> bool:
    """检测当前 FFmpeg 是否支持 NVENC 硬件编码"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"],
            capture_output=True, text=True, timeout=10
        )
        return "h264_nvenc" in result.stdout
    except Exception:
        return False


# 模块加载时检测一次，避免重复调用
_NVENC_AVAILABLE: bool = _check_nvenc()


def _get_codec_and_params(requested_codec: str) -> tuple[str, list[str]]:
    """
    根据请求的 codec 和硬件能力，返回 (实际codec, ffmpeg_params)。
    - h264_nvenc / auto  → 若 NVENC 可用则用 GPU，否则回退 libx264
    - libx264            → CPU 编码，faster preset
    """
    if requested_codec in ("h264_nvenc", "auto"):
        if _NVENC_AVAILABLE:
            print("  [gpu] 使用 NVENC 硬件加速编码 (h264_nvenc)")
            return "h264_nvenc", [
                "-preset", "p4",       # NVENC preset: p1(快)~p7(慢), p4 质量/速度平衡
                "-rc", "vbr",
                "-cq", "23",           # 质量因子，等效 CRF 23
                "-b:v", "0",
                "-maxrate:v", "12M",
                "-bufsize", "24M",
            ]
        else:
            print("  [gpu] NVENC 不可用，回退到 libx264")
            requested_codec = "libx264"

    if requested_codec == "libx264":
        cpu_count = os.cpu_count() or 4
        threads = min(cpu_count, 8)
        return "libx264", [
            "-preset", "fast",
            "-crf", "23",
            "-threads", str(threads),
        ]

    # 其他 codec（hevc_nvenc 等）直接透传
    return requested_codec, []


def _scaled(base_val: int, height: int, ref_height: int = 1080) -> int:
    """根据画面高度等比缩放，以 1080p 为基准"""
    return max(1, int(base_val * height / ref_height))


def _resolve_font(font_name: str) -> str:
    """解析字体名到实际字体文件路径（Windows / Linux 兼容）"""
    import platform

    # 1. 如果已经是存在的绝对路径，直接返回
    if os.path.isabs(font_name) and os.path.exists(font_name):
        return font_name

    # 2. 查找项目内置字体（assets/fonts/）
    _here = os.path.dirname(os.path.abspath(__file__))
    _project_root = os.path.dirname(_here)
    _assets_fonts = os.path.join(_project_root, "assets", "fonts")
    for ext in ("", ".ttf", ".ttc", ".otf"):
        candidate = os.path.join(_assets_fonts, font_name + ext)
        if os.path.exists(candidate):
            return candidate

    sys_name = platform.system()

    if sys_name == "Windows":
        font_map = {
            "Microsoft-YaHei": "msyh.ttc",
            "Microsoft-YaHei-Bold": "msyhbd.ttc",
            "Microsoft YaHei": "msyh.ttc",
            "SimHei": "simhei.ttf",
            "SimSun": "simsun.ttc",
            "KaiTi": "simkai.ttf",
        }
        fname = font_map.get(font_name, font_name)
        if not os.path.isabs(fname):
            windir = os.environ.get("WINDIR", "C:\\Windows")
            full = os.path.join(windir, "Fonts", fname)
            if os.path.exists(full):
                return full

    elif sys_name == "Linux":
        # Noto CJK（fonts-noto-cjk 安装后的常见路径）
        linux_candidates = [
            # Ubuntu/Debian: fonts-noto-cjk
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/noto-cjk/NotoSansCJKsc-Regular.otf",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            # CentOS/RHEL: google-noto-cjk
            "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
            # WQY（文泉驿）
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc",
            "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc",
        ]
        for path in linux_candidates:
            if os.path.exists(path):
                return path
        # 硬编码候选都找不到时，动态搜索（排除 emoji）
        found = _find_any_cjk_font()
        if found:
            return found

    return font_name


def _find_any_cjk_font() -> str:
    """在当前系统上找到任意可用的 CJK 文字字体，找不到返回空字符串。
    注意：会排除 emoji / color bitmap 字体（PIL 无法用来渲染普通文字）。
    优先查找项目内置的 assets/fonts/ 目录。
    """
    import glob as _glob
    _here = os.path.dirname(os.path.abspath(__file__))
    _assets_fonts = os.path.join(os.path.dirname(_here), "assets", "fonts")
    search_dirs = [
        _assets_fonts,                           # ← 优先：项目内置字体
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        os.path.expanduser("~/.fonts"),
        os.path.expanduser("~/.local/share/fonts"),
    ]
    # 文件名含这些词的直接排除（emoji / color 位图字体）
    exclude_kw = ("emoji", "color", "notocolor", "seguiemj", "symbol",
                  "webdings", "wingdings")
    # CJK 文字字体关键词
    include_kw = ("cjk", "wqy", "hans", "hant", "chinese", "zh-")

    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for ext in ("*.ttc", "*.ttf", "*.otf"):
            for f in _glob.glob(os.path.join(d, "**", ext), recursive=True):
                low = os.path.basename(f).lower()
                if any(e in low for e in exclude_kw):
                    continue
                # assets/fonts/ 目录里的字体是用户主动放置的，无需关键词过滤
                if d == _assets_fonts:
                    return f
                if any(k in low for k in include_kw):
                    return f
    # 再宽松：包含 noto+sans 但排除 emoji（系统目录）
    for d in search_dirs[1:]:
        if not os.path.isdir(d):
            continue
        for ext in ("*.ttc", "*.ttf", "*.otf"):
            for f in _glob.glob(os.path.join(d, "**", ext), recursive=True):
                low = os.path.basename(f).lower()
                if any(e in low for e in exclude_kw):
                    continue
                if "noto" in low and "sans" in low:
                    return f
    return ""


def _get_bold_font(fallback: str = "Microsoft-YaHei") -> str:
    """获取粗体字体路径，找不到则回退到任意可用 CJK 字体"""
    bold = _resolve_font("Microsoft-YaHei-Bold")
    if not os.path.exists(bold):
        bold = _resolve_font(fallback)
    if not os.path.exists(bold):
        bold = _find_any_cjk_font() or bold
    return bold


def _measure_text_width(
    text: str,
    font_path: str,
    font_size: int,
    stroke_width: int = 0,
) -> int:
    """用 Pillow 测量文本像素宽度，失败时退化为估算值"""
    if not text:
        return 0

    try:
        font_obj = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        bbox = draw.textbbox((0, 0), text, font=font_obj, stroke_width=stroke_width)
        return max(0, bbox[2] - bbox[0])
    except Exception:
        return int(len(text) * font_size * 0.6)


def _tokenize_for_wrap(text: str) -> list[str]:
    """将中英混排文本切分为换行 token，英文词尽量不断开"""
    tokens: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\n":
            tokens.append("\n")
            i += 1
            continue

        if ch.isspace():
            if tokens and tokens[-1] != " ":
                tokens.append(" ")
            i += 1
            continue

        if ch.isascii() and (ch.isalnum() or ch in "_-+/.#%:@"):
            j = i + 1
            while j < len(text):
                cj = text[j]
                if cj.isascii() and (cj.isalnum() or cj in "_-+/.#%:@"):
                    j += 1
                else:
                    break
            tokens.append(text[i:j])
            i = j
            continue

        tokens.append(ch)
        i += 1

    return tokens


def _wrap_text_to_width(
    text: str,
    font_path: str,
    font_size: int,
    max_width: int,
    stroke_width: int = 0,
) -> str:
    """按像素宽度手动换行，解决 caption 对中文换行不稳定的问题"""
    if not text:
        return text
    if max_width <= 0:
        return text

    tokens = _tokenize_for_wrap(text)
    lines: list[str] = []
    current = ""

    def _fits(candidate: str) -> bool:
        return _measure_text_width(candidate, font_path, font_size, stroke_width) <= max_width

    def _push_current() -> None:
        nonlocal current
        lines.append(current.rstrip())
        current = ""

    for token in tokens:
        if token == "\n":
            _push_current() if current else lines.append("")
            continue

        candidate = token if not current else current + token
        if _fits(candidate):
            current = candidate
            continue

        if current:
            _push_current()

        token = token.lstrip()
        if not token:
            continue

        if _fits(token):
            current = token
            continue

        # 超长 token（例如很长 URL）按字符强制拆分
        for ch in token:
            piece = ch if not current else current + ch
            if current and not _fits(piece):
                _push_current()
                current = ch
            else:
                current = piece

    if current:
        _push_current()

    wrapped = "\n".join(lines).strip()
    return wrapped or text


def _make_text_clip(
    text: str,
    font: str,
    font_size: int,
    color: str,
    max_width: int,
    duration: float,
    stroke_color: str = "black",
    stroke_width: int = 1,
    text_align: str = "center",
    max_height: int | None = None,
) -> "TextClip | None":
    """可靠文本渲染：手动换行 + label，必要时自动缩字号以避免裁剪"""
    if not text:
        return None

    resolved_font = _resolve_font(font)
    safe_max_w = max(20, int(max_width))
    fs = max(1, int(font_size))
    min_fs = min(fs, max(8, int(fs * 0.65)))
    last_error = None

    while fs >= min_fs:
        wrapped_text = _wrap_text_to_width(
            text=text,
            font_path=resolved_font,
            font_size=fs,
            max_width=safe_max_w,
            stroke_width=stroke_width,
        )
        try:
            clip = TextClip(
                text=wrapped_text,
                font=resolved_font,
                font_size=fs,
                color=color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
                method="label",
                text_align=text_align,
                interline=max(2, int(fs * 0.14)),
                margin=(0, max(2, int(fs * 0.24))),
            )
        except Exception as e:
            last_error = e
            fs -= 1
            continue

        if max_height is None or clip.h <= max_height:
            return clip.with_duration(duration)

        clip.close()
        next_fs = int(fs * 0.92)
        fs = next_fs if next_fs < fs else fs - 1

    print(f"    [warn] TextClip 失败: {last_error or '无法在目标区域内渲染文本'}")
    return None


# ===== 视觉素材路径解析 =====

def _resolve_visual_path(
    source: str,
    assets_dir: str,
    scene_id: str,
) -> str | None:
    """解析视觉素材路径，支持多种后缀自动查找
    
    查找顺序：
    1. 原始路径（source）
    2. 相对于项目根目录的路径
    3. 自动尝试添加 _icon.png / _illustration.png 后缀
    """
    if not source:
        return None
    
    # 1. 尝试原始路径
    if os.path.exists(source):
        return source
    
    # 2. 尝试相对于项目根目录
    project_root = os.path.dirname(assets_dir)
    rel_path = os.path.join(project_root, source)
    if os.path.exists(rel_path):
        return rel_path
    
    # 3. 自动查找后缀变体（解决 assets/manual/XX_name.png 不存在的情况）
    base_dir = os.path.dirname(rel_path)
    base_name = os.path.splitext(os.path.basename(source))[0]  # 去掉扩展名
    
    if os.path.isdir(base_dir):
        prefix = base_name + "_"
        candidates = []
        for f in os.listdir(base_dir):
            if f.startswith(prefix):
                ext = os.path.splitext(f)[1].lower()
                if ext in ('.png', '.jpg', '.jpeg', '.mp4'):
                    candidates.append(f)
        
        if candidates:
            # 优先选择 _icon，然后 _illustration
            for f in candidates:
                if '_icon' in f:
                    return os.path.join(base_dir, f)
            return os.path.join(base_dir, candidates[0])
    
    return None


# ===== 背景生成 =====

def _make_gradient_bg(width: int, height: int, duration: float,
                      color_top=(245, 245, 250), color_bottom=(230, 230, 240)) -> ImageClip:
    """生成浅灰渐变背景"""
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        gradient[y, :] = (r, g, b)
    return ImageClip(gradient).with_duration(duration)


# ===== 音频解析 =====

def _resolve_audio_path(scene: SceneItem, assets_dir: str) -> str | None:
    """按优先级查找音频文件: override > rvc > tts/avatar"""
    if scene.audio_override:
        if os.path.exists(scene.audio_override):
            return scene.audio_override
        project_root = os.path.dirname(assets_dir)
        rel_path = os.path.join(project_root, scene.audio_override)
        if os.path.exists(rel_path):
            return rel_path

    rvc_path = os.path.join(assets_dir, "audio_rvc", f"{scene.id}.mp3")
    if os.path.exists(rvc_path):
        return rvc_path

    for ext in (".mp3", ".wav"):
        tts_path = os.path.join(assets_dir, "audio", f"{scene.id}{ext}")
        if os.path.exists(tts_path):
            return tts_path

    return None


# ===== 视觉素材 =====

def _make_title_on_bg(
    bg_clip,
    title_text: str,
    width: int,
    height: int,
    duration: float,
    text_color: str = "white",
    font_size: int = 56,
) -> "CompositeVideoClip":
    """在背景上居中渲染标题文字（通用方法）"""
    if not title_text:
        return bg_clip

    bold_font = _get_bold_font()
    title_fs = _scaled(font_size, height)
    text_w = width - _scaled(160, height)  # 两侧留边距

    title_clip = _make_text_clip(
        text=title_text,
        font=bold_font,
        font_size=title_fs,
        color=text_color,
        max_width=text_w,
        duration=duration,
        text_align="center",
        max_height=int(height * 0.8),
    )
    if title_clip is None:
        return bg_clip

    # 将 title_clip 水平居中：先算出 x 偏移使其在画面中心
    x_pos = (width - title_clip.w) // 2
    y_pos = (height - title_clip.h) // 2

    return CompositeVideoClip([
        bg_clip,
        title_clip.with_position((x_pos, y_pos)),
    ], size=(width, height), bg_color=(0, 0, 0))


def _load_image_clip(path: str) -> "ImageClip":
    """
    PIL を経由して画像を読み込み、RGB 変換後に ImageClip を作成する。
    RGBA / Palette(P) / CMYK などの非RGB画像で ImageClip が失敗するのを防ぐ。
    """
    img = Image.open(path).convert("RGB")
    return ImageClip(np.array(img))


def _apply_ken_burns(
    path: str,
    width: int,
    height: int,
    duration: float,
    scene_id: str = "",
    motion_cfg: dict | None = None,
) -> "VideoClip":
    import hashlib

    cfg = motion_cfg or {}
    motion = (cfg.get("image_motion") or "subtle").strip().lower()
    if motion == "static":
        return _load_image_clip(path).resized((width, height)).with_duration(duration)

    zoom_delta = float(cfg.get("ken_burns_zoom", 0.06))
    pan_strength = float(cfg.get("ken_burns_pan", 0.35))
    pre_scale = float(cfg.get("ken_burns_pre_scale", 1.18))
    min_scale = 1.0 + max(0.0, zoom_delta) + 0.02
    if pre_scale < min_scale:
        pre_scale = min_scale
    dir_mode = (cfg.get("ken_burns_directions") or "cardinal").strip().lower()

    directions = [
        (0.0, 0.5, 1.0, 0.5),
        (1.0, 0.5, 0.0, 0.5),
        (0.5, 0.0, 0.5, 1.0),
        (0.5, 1.0, 0.5, 0.0),
    ]
    if dir_mode not in ("cardinal", "four"):
        directions += [
            (0.0, 0.0, 1.0, 1.0),
            (1.0, 0.0, 0.0, 1.0),
            (0.0, 1.0, 1.0, 0.0),
            (1.0, 1.0, 0.0, 0.0),
        ]

    seed = int(hashlib.md5(scene_id.encode()).hexdigest(), 16) % len(directions)
    sx0, sy0, sx1, sy1 = directions[seed]
    sx0 = 0.5 + (sx0 - 0.5) * pan_strength
    sy0 = 0.5 + (sy0 - 0.5) * pan_strength
    sx1 = 0.5 + (sx1 - 0.5) * pan_strength
    sy1 = 0.5 + (sy1 - 0.5) * pan_strength

    pre_w = int(width * pre_scale)
    pre_h = int(height * pre_scale)

    # 一次性读取高分辨率帧，避免逐帧 I/O
    img_arr = np.array(_load_image_clip(path).resized((pre_w, pre_h)).get_frame(0))

    def make_frame(t: float):
        progress = t / max(duration, 1e-3)
        p = progress * progress * (3.0 - 2.0 * progress)

        zoom = 1.0 + zoom_delta * p
        crop_w = max(1, int(width / zoom))
        crop_h = max(1, int(height / zoom))

        max_x = max(0, pre_w - crop_w)
        max_y = max(0, pre_h - crop_h)

        px = int((sx0 + (sx1 - sx0) * p) * max_x)
        py = int((sy0 + (sy1 - sy0) * p) * max_y)
        px = max(0, min(px, max_x))
        py = max(0, min(py, max_y))

        cropped = img_arr[py : py + crop_h, px : px + crop_w]
        return np.array(Image.fromarray(cropped).resize((width, height), Image.LANCZOS))

    return VideoClip(make_frame, duration=duration)


def _resolve_visual(
    scene: SceneItem,
    assets_dir: str,
    duration: float,
    target_size: tuple,
    title_font_size: int = 56,
    visual_cfg: dict | None = None,
) -> "VideoFileClip | ImageClip | None":
    """按类型和优先级加载视觉素材"""
    width, height = target_size

    if scene.visual_type == "manim":
        path = os.path.join(assets_dir, "manim", f"{scene.visual_source}.mp4")
        if os.path.exists(path):
            clip = VideoFileClip(path)
            if clip.duration < duration:
                last_frame = clip.to_ImageClip(t=clip.duration - 0.01).with_duration(
                    duration - clip.duration
                )
                clip = concatenate_videoclips([clip, last_frame])
            else:
                clip = clip.subclipped(0, duration)
            return clip.resized((width, height))
        # Manim render failed or file missing: use readable fallback card.
        fallback_text = (scene.text or scene.visual_prompt or scene.visual_source or "Visual Pending").strip()
        bg = _make_gradient_bg(width, height, duration, color_top=(32, 38, 52), color_bottom=(16, 20, 30))
        return _make_title_on_bg(
            bg,
            fallback_text,
            width,
            height,
            duration,
            text_color="white",
            font_size=max(32, int(title_font_size * 0.75)),
        )

    elif scene.visual_type == "ai_image":
        path = os.path.join(assets_dir, "images", f"{scene.id}.png")
        if os.path.exists(path):
            return _apply_ken_burns(path, width, height, duration, scene.id, visual_cfg)

    elif scene.visual_type in ("image", "clipart"):
        # 使用智能路径解析，自动查找正确后缀
        path = _resolve_visual_path(scene.visual_source, assets_dir, scene.id)
        if path:
            print(f"    → 使用素材: {path}")
            return _apply_ken_burns(path, width, height, duration, scene.id, visual_cfg)

    elif scene.visual_type == "ai_video":
        # 从 assets/videos/{scene_id}.mp4 加载用户手动放置的 AI 生成视频
        path = scene.visual_source
        if not path:
            path = os.path.join(assets_dir, "videos", f"{scene.id}.mp4")
        if path and not os.path.exists(path):
            project_root = os.path.dirname(assets_dir)
            rel_path = os.path.join(project_root, path)
            if os.path.exists(rel_path):
                path = rel_path
        if path and os.path.exists(path):
            clip = VideoFileClip(path)
            if clip.duration < duration:
                clip = clip.with_effects([vfx.Loop(duration=duration)])
            else:
                clip = clip.subclipped(0, duration)
            return clip.resized((width, height))
        # 文件缺失：尝试 _fallback.png（ai_image fallback），否则显示占位卡
        fallback_img = os.path.join(assets_dir, "images", f"{scene.id}_fallback.png")
        if os.path.exists(fallback_img):
            return _apply_ken_burns(fallback_img, width, height, duration, scene.id, visual_cfg)
        # 最终兜底：深色占位卡 + 提示文字
        fallback_text = f"[AI Video Pending]\n{(scene.text or scene.id)[:40]}"
        bg = _make_gradient_bg(width, height, duration, color_top=(20, 30, 50), color_bottom=(10, 15, 30))
        return _make_title_on_bg(bg, fallback_text, width, height, duration,
                                  text_color="#aabbcc", font_size=max(28, int(title_font_size * 0.65)))

    elif scene.visual_type == "video":
        path = scene.visual_source
        if path:
            if not os.path.exists(path):
                project_root = os.path.dirname(assets_dir)
                rel_path = os.path.join(project_root, path)
                if os.path.exists(rel_path):
                    path = rel_path
            if os.path.exists(path):
                clip = VideoFileClip(path)
                if clip.duration < duration:
                    clip = clip.with_effects([vfx.Loop(duration=duration)])
                else:
                    clip = clip.subclipped(0, duration)
                return clip.resized((width, height))

    elif scene.visual_type == "solid_bg":
        # 支持 LLM 指定主题色（visual.color 字段，hex 格式如 "#0d1b2a"）
        if getattr(scene, "visual_color", None):
            try:
                hex_c = scene.visual_color.lstrip("#")
                r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
                color_top = (r, g, b)
                color_bottom = (max(0, r - 18), max(0, g - 18), max(0, b - 18))
                text_color = "white"
            except Exception:
                color_top, color_bottom, text_color = (245, 245, 250), (230, 230, 240), "#333333"
        else:
            color_top, color_bottom, text_color = (245, 245, 250), (230, 230, 240), "#333333"
        bg = _make_gradient_bg(width, height, duration, color_top, color_bottom)
        return _make_title_on_bg(bg, scene.visual_prompt, width, height, duration,
                                  text_color=text_color, font_size=title_font_size)

    elif scene.visual_type == "title_card":
        # 用暗色渐变替代纯黑，保留“章节卡”风格同时减轻开场压黑感
        bg = _make_gradient_bg(
            width,
            height,
            duration,
            color_top=(18, 18, 24),
            color_bottom=(6, 6, 10),
        )
        return _make_title_on_bg(bg, scene.visual_source, width, height, duration,
                                  text_color="white", font_size=title_font_size)

    # Fallback
    if scene.visual_fallback and os.path.exists(scene.visual_fallback):
        print(f"    → 使用 fallback: {scene.visual_fallback}")
        clip = ImageClip(scene.visual_fallback).with_duration(duration)
        return clip.resized((width, height))

    return None


# ===== Avatar 叠加 =====

def _overlay_avatar(
    base_clip,
    scene: SceneItem,
    assets_dir: str,
    target_size: tuple,
    avatar_margin: int = 20,
) -> "CompositeVideoClip":
    """将 avatar 片段叠加到主视觉上"""
    width, height = target_size
    duration = base_clip.duration

    avatar_path = os.path.join(assets_dir, "avatar", f"{scene.id}_avatar.mp4")
    if not os.path.exists(avatar_path):
        return base_clip

    avatar_clip = VideoFileClip(avatar_path)

    if avatar_clip.duration < duration:
        avatar_clip = avatar_clip.with_effects([vfx.Loop(duration=duration)])
    elif avatar_clip.duration > duration:
        avatar_clip = avatar_clip.subclipped(0, duration)

    mode = scene.avatar_mode
    scale = scene.avatar_scale

    if mode == "fullscreen":
        return avatar_clip.resized((width, height))

    elif mode.startswith("split_"):
        avatar_w = int(width * 0.35)
        content_w = width - avatar_w
        avatar_clip = avatar_clip.resized((avatar_w, height))
        base_resized = base_clip.resized((content_w, height))

        if mode == "split_right":
            return CompositeVideoClip([
                base_resized.with_position((0, 0)),
                avatar_clip.with_position((content_w, 0)),
            ], size=(width, height), bg_color=(0, 0, 0))
        else:
            return CompositeVideoClip([
                avatar_clip.with_position((0, 0)),
                base_resized.with_position((avatar_w, 0)),
            ], size=(width, height), bg_color=(0, 0, 0))

    elif mode.startswith("pip_"):
        pip_h = int(height * scale)
        pip_w = int(pip_h * avatar_clip.w / avatar_clip.h)
        avatar_clip = avatar_clip.resized((pip_w, pip_h))

        subtitle_reserve = int(height * 0.15)
        positions = {
            "pip_br": (width - pip_w - avatar_margin, height - pip_h - subtitle_reserve),
            "pip_bl": (avatar_margin, height - pip_h - subtitle_reserve),
            "pip_tr": (width - pip_w - avatar_margin, avatar_margin),
            "pip_tl": (avatar_margin, avatar_margin),
        }
        pos = positions.get(mode, positions["pip_br"])

        # 软阴影：在 Avatar 图层下放一个比 Avatar 大 12px 的半透明黑色矩形
        shadow_pad = 12
        shadow = (
            ColorClip(size=(pip_w + shadow_pad * 2, pip_h + shadow_pad * 2), color=(0, 0, 0))
            .with_duration(duration)
            .with_opacity(0.45)
        )
        shadow_pos = (max(0, pos[0] - shadow_pad), max(0, pos[1] - shadow_pad))

        return CompositeVideoClip([
            base_clip,
            shadow.with_position(shadow_pos),
            avatar_clip.with_position(pos),
        ], size=(width, height), bg_color=(0, 0, 0))

    return base_clip


# ===== 字幕烧入 =====

def _make_subtitle_clip(
    text: str,
    duration: float,
    width: int,
    height: int,
    font: str = "Microsoft-YaHei",
    font_size: int = 32,
    color: str = "white",
    bg_color: str = None,
    bg_opacity: float = 0.5,
    content_x: int = 0,
    content_w: int = None,
) -> "CompositeVideoClip | None":
    """字幕渲染：简单可靠版。method=caption 自动换行，ColorClip 半透明底条。"""
    if content_w is None:
        content_w = width

    bold_font = _get_bold_font(font)
    actual_fs = _scaled(font_size, height)
    margin_x = _scaled(80, height)
    max_w = min(content_w, max(_scaled(240, height), content_w - margin_x * 2))
    max_h = int(height * 0.38)

    txt_clip = _make_text_clip(
        text=text,
        font=bold_font,
        font_size=actual_fs,
        color=color,
        max_width=max_w,
        duration=duration,
        stroke_color="black",
        stroke_width=1,
        text_align="center",
        max_height=max_h,
    )
    if txt_clip is None:
        return None

    bottom_margin = int(height * 0.06)
    y_pos = max(0, height - txt_clip.h - bottom_margin)
    txt_x = content_x + (content_w - txt_clip.w) // 2

    layers = []

    # 半透明底条（用 ColorClip + with_opacity，比 RGBA numpy 更可靠）
    if bg_opacity > 0:
        color_map = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "gray": (128, 128, 128),
            "grey": (128, 128, 128),
        }
        bar_color = color_map.get((bg_color or "black").lower(), (0, 0, 0))
        pad_v = _scaled(8, height)
        pad_h = _scaled(20, height)
        bar_h = txt_clip.h + pad_v * 2
        bar_w = min(txt_clip.w + pad_h * 2, content_w)
        bar_x = content_x + (content_w - bar_w) // 2
        bar_y = y_pos - pad_v
        if bar_y < 0:
            bar_h = max(1, bar_h + bar_y)
            bar_y = 0
        if bar_y + bar_h > height:
            bar_h = max(1, height - bar_y)
        bar = (
            ColorClip(size=(bar_w, bar_h), color=bar_color)
            .with_duration(duration)
            .with_opacity(bg_opacity)
        )
        layers.append(bar.with_position((bar_x, bar_y)))

    layers.append(txt_clip.with_position((txt_x, y_pos)))

    # 不传 size= ：让 MoviePy 从各子层推断尺寸，避免它内部创建
    # ColorClip(1920×1080, float64 mask) 占用 15.8 MiB/场景 → 内存耗尽
    result = CompositeVideoClip(layers)
    # 字幕淡入（0.2s），场景极短时收窄到 10% 时长，保证不超出
    fade_dur = min(0.2, duration * 0.1)
    if fade_dur > 0.05:
        result = result.with_effects([vfx.FadeIn(fade_dur)])
    return result


# ===== 主合成函数 =====

def _validate_audio(path: str) -> bool:
    try:
        return os.path.exists(path) and os.path.getsize(path) > 500
    except:
        return False


def _resolve_transition_mode(scene_transition: str | None, default_transition: str) -> str:
    valid = {"crossfade", "fade_black", "cut"}
    if isinstance(scene_transition, str):
        mode = scene_transition.strip().lower()
        if mode in valid:
            return mode
    default_mode = (default_transition or "").strip().lower()
    return default_mode if default_mode in valid else "crossfade"


def _compute_transition_span(
    left_clip,
    right_clip,
    wanted: float,
) -> float:
    if wanted <= 0:
        return 0.0
    left_d = float(getattr(left_clip, "duration", 0) or 0)
    right_d = float(getattr(right_clip, "duration", 0) or 0)
    if left_d <= 0 or right_d <= 0:
        return 0.0
    return min(wanted, left_d * 0.45, right_d * 0.45)


def _concat_with_scene_transitions(
    clips: List,
    scenes: List,
    default_transition: str,
    transition_duration: float,
):
    """Per-scene transitions on a single timeline to avoid deep nested clips."""
    if not clips:
        return None
    if len(clips) == 1:
        return clips[0]

    base_td = max(0.0, float(transition_duration or 0))

    # Each entry is [clip, start_time]. Build timeline first, compose once.
    arranged = [[clips[0], 0.0]]
    first_duration = float(getattr(clips[0], "duration", 0) or 0)
    timeline_end = max(0.0, first_duration)

    for i in range(1, len(clips)):
        right = clips[i]
        left = arranged[-1][0]
        prev_scene = scenes[i - 1] if i - 1 < len(scenes) else None
        mode = _resolve_transition_mode(getattr(prev_scene, "transition", None), default_transition)
        span = _compute_transition_span(left, right, base_td)

        if mode == "crossfade" and span > 0:
            arranged[-1][0] = left.with_effects([vfx.CrossFadeOut(span)])
            right = right.with_effects([vfx.CrossFadeIn(span)])
            start_t = max(0.0, timeline_end - span)
        elif mode == "fade_black" and span > 0:
            arranged[-1][0] = left.with_effects([vfx.FadeOut(span)])
            right = right.with_effects([vfx.FadeIn(span)])
            start_t = timeline_end
        else:
            start_t = timeline_end

        arranged.append([right, start_t])
        right_d = float(getattr(right, "duration", 0) or 0)
        timeline_end = max(timeline_end, start_t + right_d)

    timeline_clips = [clip.with_start(start_t) for clip, start_t in arranged]
    comp_w = int(getattr(clips[0], "w", 0) or 0)
    comp_h = int(getattr(clips[0], "h", 0) or 0)
    if comp_w > 0 and comp_h > 0:
        return CompositeVideoClip(timeline_clips, size=(comp_w, comp_h), bg_color=(0, 0, 0)).with_duration(timeline_end)
    return CompositeVideoClip(timeline_clips).with_duration(timeline_end)


def assemble_video(
    scenes: List,
    assets_dir: str,
    output_path: str,
    width: int = 1920,
    height: int = 1080,
    fps: int = 30,
    codec: str = "libx264",
    subtitle_cfg: dict = None,
    avatar_cfg: dict = None,
    visual_cfg: dict = None,
    transition: str = "crossfade",
    transition_duration: float = 0.5,
    default_duration: float = 2.5,
) -> str | None:
    """
    v2.4: 修复标题偏移 + 字幕截断 + 重影 + 字号自适应
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    sub_cfg = subtitle_cfg or {}
    sub_enabled = sub_cfg.get("enabled", True)
    avt_cfg = avatar_cfg or {}
    avatar_margin = avt_cfg.get("margin", 20)
    vis_cfg = visual_cfg or {}
    target_size = (width, height)

    final_clips = []
    print(f"\n开始合成任务: {len(scenes)} 个场景 (分辨率: {width}x{height})")
    
    # 动态加载 config 用于判断是不是 ChatTTS 
    import sys
    from config import load_config
    cfg = load_config()
    is_chattts = (cfg.tts.provider == "chattts")
    title_duration = getattr(cfg.video, "default_title_duration", 3.0)
    solid_bg_duration = getattr(cfg.video, "default_solid_bg_duration", 2.5)

    for i, scene in enumerate(scenes):
        print(f"  正在处理 [{i+1}/{len(scenes)}] ID: {scene.id} ...")

        current_audio = None
        current_duration = default_duration

        # 1. 音频
        audio_path = _resolve_audio_path(scene, assets_dir)
        if audio_path and _validate_audio(audio_path):
            try:
                current_audio = AudioFileClip(audio_path)
                
                # 如果是 ChatTTS 且非覆盖音频，强制追加静音尾缀(句间停顿)
                if is_chattts and (not scene.audio_override) and ("audio_rvc" not in audio_path):
                    padding = getattr(cfg.tts, "padding_duration", 0.3)
                    if padding > 0:
                        from moviepy.audio.AudioClip import AudioArrayClip
                        silence = AudioArrayClip(np.zeros((int(44100 * padding), 2)), fps=44100)
                        current_audio = concatenate_audioclips([current_audio, silence])

                current_duration = current_audio.duration
            except Exception as e:
                print(f"    [!] 音频加载失败 ({scene.id}): {e}")
                current_audio = None
        else:
            if not scene.text:
                if scene.visual_type == "title_card":
                    current_duration = title_duration
                elif scene.visual_type == "solid_bg":
                    current_duration = solid_bg_duration
            print(f"    [i] 未找到音频或音频损坏，使用默认时长 {current_duration}s")

        # 2. 视觉
        visual_clip = _resolve_visual(
            scene,
            assets_dir,
            current_duration,
            target_size,
            title_font_size=sub_cfg.get("title_font_size", 56),
            visual_cfg=vis_cfg,
        )
        if visual_clip is None:
            visual_clip = _make_gradient_bg(width, height, current_duration)

        # 3. Avatar
        if scene.avatar_mode != "hidden":
            try:
                new_visual = _overlay_avatar(
                    visual_clip, scene, assets_dir, target_size, avatar_margin
                )
                if new_visual is not visual_clip:
                    # avatar 叠加创建了新对象，旧 visual_clip 可以释放
                    try:
                        visual_clip.close()
                    except Exception:
                        pass
                visual_clip = new_visual
            except Exception as e:
                print(f"    [!] Avatar 叠加失败: {e}")

        # 4. 字幕（split 模式时字幕只在内容区显示，避让 avatar）
        if sub_enabled and scene.text:
            clean_text = scene.text.replace("*", "").replace("#", "").replace("`", "")

            avatar_w_split = int(width * 0.35)
            if scene.avatar_mode == "split_left":
                sub_content_x = avatar_w_split
                sub_content_w = width - avatar_w_split
            elif scene.avatar_mode == "split_right":
                sub_content_x = 0
                sub_content_w = width - avatar_w_split
            else:
                sub_content_x = 0
                sub_content_w = width

            subtitle = _make_subtitle_clip(
                text=clean_text,
                duration=current_duration,
                width=width,
                height=height,
                font=sub_cfg.get("font", "Microsoft-YaHei"),
                font_size=sub_cfg.get("font_size", 32),
                color=sub_cfg.get("color", "white"),
                bg_color=sub_cfg.get("bg_color", "black"),
                bg_opacity=sub_cfg.get("bg_opacity", 0.5),
                content_x=sub_content_x,
                content_w=sub_content_w,
            )
            if subtitle is not None:
                # 展平字幕层，避免 CompositeVideoClip 嵌套导致 MoviePy 内部
                # 用 int64 分配巨大背景 ColorClip（63 MiB/场景 → 内存耗尽）
                sub_layers = list(getattr(subtitle, "clips", [subtitle]))
                visual_clip = CompositeVideoClip(
                    [visual_clip] + sub_layers,
                    size=(width, height), bg_color=(0, 0, 0)
                )
                # 移除 subtitle.close() 防止意外删除关联内存
                pass


        # 5. 合并
        visual_clip = visual_clip.with_duration(current_duration)
        if current_audio:
            visual_clip = visual_clip.with_audio(current_audio)
        final_clips.append(visual_clip)
        # 每处理完一个场景立即回收，防止碎片化内存累积到后期 OOM
        gc.collect()

    if not final_clips:
        print("[error] 没有任何片段成功生成")
        return None

    # 6. 转场与拼接
    try:
        print(f"\n正在进行拼接渲染 (逐场景转场，默认: {transition})...")
        final_video = _concat_with_scene_transitions(
            final_clips,
            scenes,
            default_transition=transition,
            transition_duration=transition_duration,
        )
        if final_video is None:
            print("[error] 拼接失败：没有可用片段")
            return None

        render_seconds = float(getattr(final_video, "duration", 0) or 0)
        est_frames = int(max(0, round(render_seconds * max(1, int(fps)))))
        print(f"  [render] 预计渲染时长: {render_seconds:.1f}s, 约 {est_frames} 帧 (fps={fps})")

        actual_codec, extra_params = _get_codec_and_params(codec)
        final_video.write_videofile(
            output_path,
            fps=fps,
            codec=actual_codec,
            audio_codec="aac",
            temp_audiofile=os.path.join(os.path.dirname(output_path), "temp-audio.m4a"),
            remove_temp=False,
            logger="bar",
            ffmpeg_params=extra_params,
            threads=1,  # 关键修复：限制多线程以防 1080p 多轨合成时 numpy OOM 内存泄漏
        )
    finally:
        print("清理内存中...")
        if 'final_video' in locals():
            final_video.close()
        for c in final_clips:
            try:
                c.close()
            except:
                pass
        gc.collect()
        temp_audio = os.path.join(os.path.dirname(output_path), "temp-audio.m4a")
        try:
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
        except PermissionError:
            pass

    print(f"视频生成成功: {output_path}")
    return output_path
