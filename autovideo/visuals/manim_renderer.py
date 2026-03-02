"""Manim renderer for all `visual.type == "manim"` scenes."""

import glob
import os
import shutil
import subprocess
import sys
from typing import List

from parser.script_parser import SceneItem
from visuals.manim_generator import (
    append_to_manim_scenes,
    generate_manim_code,
    save_scene_to_library,
    refine_manim_scene,
)


QUALITY_MAP = {
    "l": "480p15",
    "m": "720p30",
    "h": "1080p60",
    "k": "2160p60",
}


def _render_failure_hint(stderr: str) -> str:
    low = (stderr or "").lower()
    if "could not find eye" in low or ".svg" in low:
        return "Detected missing SVG asset. Use built-in shapes instead of SVGMobject."
    if "latex" in low or "xelatex" in low or "dvisvgm" in low:
        return "Detected LaTeX dependency. Replace Tex/MathTex with Text (unicode symbols)."
    if "winerror 2" in low:
        return "Missing external executable. Usually caused by scene code relying on unavailable tools."
    if "no module named manim" in low:
        return "Manim is not installed in the current Python environment."
    return ""


def _manim_command(quality: str, scenes_file: str, class_name: str) -> list[str]:
    if shutil.which("manim"):
        return ["manim", "render", f"-q{quality}", "--format", "mp4", scenes_file, class_name]
    return [sys.executable, "-m", "manim", "render", f"-q{quality}", "--format", "mp4", scenes_file, class_name]


def render_manim_scenes(
    scenes: List[SceneItem],
    output_dir: str,
    scenes_file: str = None,
    quality: str = "m",
    project_name: str | None = None,
) -> dict:
    """
    Render all manim scenes and return mapping: {scene_class: output_video_path}.
    """
    os.makedirs(output_dir, exist_ok=True)
    result = {}

    visuals_dir = os.path.dirname(os.path.abspath(__file__))

    if scenes_file is None:
        scenes_file = os.path.join(visuals_dir, "manim_scenes.py")

    # 项目级 generated_scenes 目录（如果提供了 project_name，则归档到子目录）
    generated_root = os.path.join(visuals_dir, "generated_scenes")
    if project_name:
        generated_dir = os.path.join(generated_root, project_name)
    else:
        generated_dir = generated_root

    manim_scenes = [s for s in scenes if s.visual_type == "manim" and s.visual_source]
    if not manim_scenes:
        return result

    # De-dup by class name. Keep last prompt.
    class_map = {s.visual_source: (s.visual_prompt or s.text or "") for s in manim_scenes}

    for class_name, prompt in class_map.items():
        target_path = os.path.join(output_dir, f"{class_name}.mp4")

        if os.path.exists(target_path):
            print(f"  [{class_name}] 已存在，跳过")
            result[class_name] = target_path
            continue

        # 默认从集中定义文件渲染；如果是自动生成的 Scene，则改为使用独立文件
        scene_source_file = scenes_file

        # 1. 优先检查项目专属 generated_scenes 目录中是否已有预生成的 Scene 文件
        pregen_path = os.path.join(generated_dir, f"{class_name}.py")
        if os.path.exists(pregen_path):
            scene_source_file = pregen_path
        else:
            # 2. 否则回退到集中 manim_scenes.py，必要时自动生成到项目目录
            with open(scenes_file, "r", encoding="utf-8") as f:
                content = f.read()

            if f"class {class_name}(Scene):" not in content and f"class {class_name}(" not in content:
                print(f"  [{class_name}] 未找到定义，正在自动生成代码...")
                if not prompt:
                    print(f"    [error] 缺少 prompt，无法生成 {class_name}")
                    continue
                try:
                    # 使用多轮生成 + 修正逻辑，尽量在构建阶段把常见错误修掉
                    code = refine_manim_scene(class_name, prompt)
                    # 保存为项目专属的独立 Scene 文件
                    scene_source_file = save_scene_to_library(code, class_name, base_dir=generated_dir)
                except Exception as e:
                    print(f"    [error] 自动生成失败: {e}")
                    continue

        print(f"  [{class_name}] 渲染中...")

        try:
            cmd = _manim_command(quality, scene_source_file, class_name)
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            print(f"  [{class_name}] 渲染超时 (>300s)")
            continue
        except FileNotFoundError:
            print("  [error] manim 命令不可用，请确认环境已安装 manim")
            break

        if proc.returncode != 0:
            err_text = (proc.stderr or proc.stdout or "").strip() or "(no stderr/stdout)"
            print(f"  [{class_name}] 渲染失败:")
            print(f"    {err_text[-1200:]}")
            hint = _render_failure_hint(err_text)
            if hint:
                print(f"    [hint] {hint}")
            continue

        quality_dir = QUALITY_MAP.get(quality, "720p30")
        search_roots = [
            os.getcwd(),
            os.path.dirname(scenes_file),
            os.path.dirname(os.path.dirname(scenes_file)),
        ]

        rendered = []
        for root in search_roots:
            media_dir = os.path.join(root, "media", "videos", "manim_scenes", quality_dir)
            rendered = glob.glob(os.path.join(media_dir, f"{class_name}*.mp4"))
            if rendered:
                break

        if not rendered:
            for root in search_roots:
                rendered = glob.glob(os.path.join(root, "media", "**", f"{class_name}*.mp4"), recursive=True)
                if rendered:
                    break

        if not rendered:
            print(f"  [{class_name}] 渲染成功但未找到输出文件")
            continue

        shutil.copy2(rendered[0], target_path)
        result[class_name] = target_path
        print(f"  [{class_name}] 渲染完成 -> {target_path}")

    return result


if __name__ == "__main__":
    print("Manim renderer")
    print("usage: manim -qm visuals/manim_scenes.py TokenizationScene")
