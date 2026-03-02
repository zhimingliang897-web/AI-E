"""Split full avatar video into per-scene clips."""

import os
from typing import List, Optional

from moviepy import AudioFileClip, VideoFileClip


def get_scene_durations(scenes, assets_dir: str) -> List[float]:
    """
    Resolve duration for each scene from audio files:
    override > audio_rvc > audio > text-length estimate.
    """
    durations = []
    for scene in scenes:
        audio_path = None

        if scene.audio_override and os.path.exists(scene.audio_override):
            audio_path = scene.audio_override
        else:
            for subdir in ("audio_rvc", "audio"):
                for ext in (".mp3", ".wav"):
                    p = os.path.join(assets_dir, subdir, f"{scene.id}{ext}")
                    if os.path.exists(p):
                        audio_path = p
                        break
                if audio_path:
                    break

        if audio_path and os.path.getsize(audio_path) > 0:
            clip = AudioFileClip(audio_path)
            durations.append(float(clip.duration))
            clip.close()
        else:
            estimated = max(3.0, len(scene.text or "") / 4.0)
            durations.append(float(estimated))

    return durations


def split_avatar_video(
    avatar_video_path: str,
    avatar_audio_path: Optional[str],
    scenes,
    assets_dir: str,
    output_dir: str,
) -> dict:
    """
    Slice full avatar video into visual-only scene clips.
    Returns: {scene_id: clip_path}
    """
    _ = avatar_audio_path  # reserved for future use
    os.makedirs(output_dir, exist_ok=True)
    result = {}

    if not os.path.exists(avatar_video_path):
        print(f"[error] Avatar 视频不存在: {avatar_video_path}")
        return result

    durations = get_scene_durations(scenes, assets_dir)
    total_needed = sum(durations)

    avatar_clip = VideoFileClip(avatar_video_path)
    avatar_duration = float(avatar_clip.duration or 0.0)
    avatar_fps = int(getattr(avatar_clip, "fps", 25) or 25)

    if avatar_duration < total_needed:
        print(f"  [warn] Avatar 视频 ({avatar_duration:.1f}s) 短于总需求 ({total_needed:.1f}s)")
        print("         超出部分将使用 avatar 最后一帧补齐")

    current_time = 0.0
    try:
        for scene, dur in zip(scenes, durations):
            if scene.avatar_mode == "hidden":
                current_time += dur
                continue

            output_path = os.path.join(output_dir, f"{scene.id}_avatar.mp4")

            if os.path.exists(output_path):
                print(f"  [{scene.id}] avatar 片段已存在，跳过")
                result[scene.id] = output_path
                current_time += dur
                continue

            end_time = current_time + dur

            if current_time >= avatar_duration - 0.1:
                freeze_t = max(0.0, avatar_duration - 0.5)
                try:
                    freeze_clip = avatar_clip.to_ImageClip(t=freeze_t).with_duration(dur)
                except Exception:
                    # Fallback if that still fails
                    freeze_t = max(0.0, avatar_duration - 1.0)
                    freeze_clip = avatar_clip.to_ImageClip(t=freeze_t).with_duration(dur)
                freeze_clip.write_videofile(
                    output_path,
                    fps=avatar_fps,
                    codec="libx264",
                    audio=False,
                    logger=None,
                )
                freeze_clip.close()
                result[scene.id] = output_path
                print(f"  [{scene.id}] avatar 视频已用完，使用最后一帧补齐 ({dur:.1f}s)")
                current_time = end_time
                continue

            actual_end = min(end_time, avatar_duration)
            clip = avatar_clip.subclipped(current_time, actual_end).without_audio()
            clip.write_videofile(
                output_path,
                fps=avatar_fps,
                codec="libx264",
                audio=False,
                logger=None,
            )
            clip.close()
            result[scene.id] = output_path
            print(f"  [{scene.id}] avatar 片段 ({current_time:.1f}s-{actual_end:.1f}s) -> {output_path}")

            current_time = end_time
    finally:
        avatar_clip.close()

    return result


if __name__ == "__main__":
    print("Avatar splitter: use via pipeline")
    print("usage: python pipeline.py build --script script.json")
