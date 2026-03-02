"""SRT 字幕生成器 - 根据音频时长生成外挂字幕文件"""

import os
from typing import List

from moviepy import AudioFileClip

from parser.script_parser import SceneItem


def _format_timestamp(seconds: float) -> str:
    """将秒数转为 SRT 时间戳格式 HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def generate_srt(
    scenes: List[SceneItem],
    assets_dir: str,
    output_path: str,
) -> str | None:
    """生成 SRT 字幕文件，返回输出路径"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    entries = []
    current_time = 0.0
    index = 1

    for scene in scenes:
        # 查找对应音频来获取实际时长
        audio_path = None
        for subdir in ("audio_rvc", "audio"):
            p = os.path.join(assets_dir, subdir, f"{scene.id}.mp3")
            if os.path.exists(p):
                audio_path = p
                break

        if scene.audio_override and os.path.exists(scene.audio_override):
            audio_path = scene.audio_override

        if not audio_path or os.path.getsize(audio_path) == 0:
            continue

        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()

        start = current_time
        end = current_time + duration

        # 清洗文本
        clean_text = scene.text.replace("*", "").replace("#", "").replace("`", "")
        entry = f"{index}\n{_format_timestamp(start)} --> {_format_timestamp(end)}\n{clean_text}\n"
        entries.append(entry)

        current_time = end
        index += 1

    if not entries:
        print("  [warn] 没有字幕条目")
        return None

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(entries))

    print(f"  字幕生成完成 → {output_path} ({index - 1} 条)")
    return output_path
