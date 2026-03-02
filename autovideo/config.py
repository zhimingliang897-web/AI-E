"""全局配置管理 - 读取 config.yaml 并提供统一访问接口"""

import os
import yaml
from dataclasses import dataclass, field
from typing import Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class LLMConfig:
    enabled: bool = True
    provider: str = "qwen"
    api_key: str = ""
    base_url: str = ""
    model: str = "qwen-plus"


@dataclass
class ImageGenConfig:
    enabled: bool = True
    provider: str = "dashscope"
    api_key: str = ""
    base_url: str = ""
    model: str = "wanx2.1-t2i-turbo"
    max_calls: int = 50


@dataclass
class TTSConfig:
    enabled: bool = True
    provider: str = "edge"  # edge / chattts
    voice: str = "zh-CN-YunxiNeural"
    rate: str = "+0%"
    pitch: str = "+0Hz"
    # ChatTTS 专用参数
    seed: int = 2222       # 音色种子
    speed: int = 5         # 语速 1-9
    oral: int = 2          # 口语化程度 0-9
    laugh: int = 0         # 笑声程度 0-2
    break_: int = 4        # 停顿程度 0-7
    padding_duration: float = 0.3 # 句间静音停顿补丁


@dataclass
class RVCConfig:
    enabled: bool = False
    api_url: str = "http://127.0.0.1:7897"
    model_name: str = "my_voice"


@dataclass
class ManimConfig:
    enabled: bool = True
    quality: str = "m"


@dataclass
class AvatarConfig:
    enabled: bool = False
    video_path: str = ""           # 完整 avatar 视频路径
    audio_path: str = ""           # avatar 配套音频路径（为空则从视频提取）
    default_mode: str = "pip_br"   # 默认布局: pip_br/pip_bl/fullscreen/hidden
    default_scale: float = 0.3     # 画中画缩放比例
    margin: int = 20               # 画中画边距(px)


@dataclass
class SubtitleConfig:
    enabled: bool = True
    font: str = "Microsoft-YaHei"  # 中文字体
    font_size: int = 36            # 旁白字幕字号（1080p 建议）
    title_font_size: int = 64      # 标题卡字号（solid_bg / title_card）
    color: str = "white"
    bg_color: str = "black"
    bg_opacity: float = 0.4
    position: str = "bottom"       # bottom / center


@dataclass
class VideoConfig:
    width: int = 1920
    height: int = 1080
    fps: int = 30
    codec: str = "libx264"
    transition: str = "crossfade"  # crossfade / fade_black / cut
    transition_duration: float = 0.5
    default_duration: float = 2.5
    default_title_duration: float = 3.0
    default_solid_bg_duration: float = 2.5


@dataclass
class VisualConfig:
    image_motion: str = "subtle"
    ken_burns_zoom: float = 0.06
    ken_burns_pan: float = 0.35
    ken_burns_pre_scale: float = 1.18
    ken_burns_directions: str = "cardinal"


@dataclass
class PathsConfig:
    assets: str = "assets"
    output: str = "output"
    scripts: str = "scripts"

    def resolve(self, base: str) -> "PathsConfig":
        """将相对路径转为绝对路径"""
        self.assets = os.path.join(base, self.assets)
        self.output = os.path.join(base, self.output)
        self.scripts = os.path.join(base, self.scripts)
        return self


@dataclass
class PixabayConfig:
    api_key: str = ""  # 免费注册: https://pixabay.com/api/docs/


@dataclass
class Config:
    llm: LLMConfig = field(default_factory=LLMConfig)
    image_gen: ImageGenConfig = field(default_factory=ImageGenConfig)
    tts: TTSConfig = field(default_factory=TTSConfig)
    rvc: RVCConfig = field(default_factory=RVCConfig)
    manim: ManimConfig = field(default_factory=ManimConfig)
    avatar: AvatarConfig = field(default_factory=AvatarConfig)
    subtitle: SubtitleConfig = field(default_factory=SubtitleConfig)
    video: VideoConfig = field(default_factory=VideoConfig)
    visual: VisualConfig = field(default_factory=VisualConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)
    pixabay: PixabayConfig = field(default_factory=PixabayConfig)


def load_config(config_path: Optional[str] = None) -> Config:
    """加载配置文件，不存在则使用默认值"""
    if config_path is None:
        config_path = os.path.join(BASE_DIR, "config.yaml")

    cfg = Config()

    if not os.path.exists(config_path):
        print(f"[warn] 配置文件 {config_path} 不存在，使用默认配置")
        print(f"[warn] 请复制 config.example.yaml 为 config.yaml 并填入 API Key")
        cfg.paths.resolve(BASE_DIR)
        return cfg

    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    def _fill(dc_class, data: dict):
        """用 dict 填充 dataclass，忽略多余字段"""
        if not data:
            return dc_class()
        valid = {k: v for k, v in data.items() if k in dc_class.__dataclass_fields__}
        return dc_class(**valid)

    cfg.llm = _fill(LLMConfig, raw.get("llm"))
    cfg.image_gen = _fill(ImageGenConfig, raw.get("image_gen"))
    cfg.tts = _fill(TTSConfig, raw.get("tts"))
    cfg.rvc = _fill(RVCConfig, raw.get("rvc"))
    cfg.manim = _fill(ManimConfig, raw.get("manim"))
    cfg.avatar = _fill(AvatarConfig, raw.get("avatar"))
    cfg.subtitle = _fill(SubtitleConfig, raw.get("subtitle"))
    cfg.video = _fill(VideoConfig, raw.get("video"))
    cfg.visual = _fill(VisualConfig, raw.get("visual"))
    cfg.paths = _fill(PathsConfig, raw.get("paths"))
    cfg.paths.resolve(BASE_DIR)
    cfg.pixabay = _fill(PixabayConfig, raw.get("pixabay"))

    return cfg


def set_project_dir(cfg: Config, project_dir: str):
    """
    将配置中的路径重定向到项目目录下。
    例如: assets -> project_dir/assets, output -> project_dir/output
    """
    abs_project_dir = os.path.abspath(project_dir)

    # 重定向 paths
    cfg.paths.assets = os.path.join(abs_project_dir, "assets")
    cfg.paths.output = os.path.join(abs_project_dir, "output")
    cfg.paths.scripts = abs_project_dir  # 脚本就在项目根目录

    # 确保文件夹存在
    os.makedirs(cfg.paths.assets, exist_ok=True)
    os.makedirs(cfg.paths.output, exist_ok=True)
