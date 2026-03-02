"""
Manim 场景生成/修正 测试工具

用法：
  1）针对单个 Scene 交互测试：
        python tools/manim_test.py

  2）针对整个脚本 script.json 批量测试：
        python tools/manim_test.py scripts/your_script.json
        python tools/manim_test.py scripts/your_script.json --render   # 同时做一次低清渲染

功能：
  - 交互式输入 Scene 类名 和 中文描述；
  - 或指定 script.json，批量对所有 visual.type == "manim" 的场景：
        * 使用 refine_manim_scene 做多轮生成 + 修正；
        * 将结果保存到 visuals/generated_scenes/<ClassName>.py；
        * 可选：调用 manim 渲染一次，快速验证是否能跑通。
"""

import os
import shutil
import subprocess
import sys
from typing import List

# 确保可以导入项目模块
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from parser.script_parser import SceneItem, parse_script  # noqa: E402
from visuals.manim_generator import refine_manim_scene, save_scene_to_library  # noqa: E402


def _manim_command(quality: str, scenes_file: str, class_name: str) -> list[str]:
    """
    构造 manim 渲染命令（与生产代码保持一致的调用方式）。
    """
    if shutil.which("manim"):
        return ["manim", "render", f"-q{quality}", "--format", "mp4", scenes_file, class_name]
    return [sys.executable, "-m", "manim", "render", f"-q{quality}", "--format", "mp4", scenes_file, class_name]


def interactive_once():
    """
    单次交互测试：输入类名 + 描述，生成并可选渲染。
    """
    print("\n" + "═" * 60)
    print("  🎬  Manim 场景生成/修正 测试")
    print("═" * 60)

    class_name = input("请输入 Scene 类名（例如: DemoScene）: ").strip()
    if not class_name:
        print("未输入类名，退出。")
        return

    print("\n请输入这个动画的大致中文描述（多行，结束后按 Ctrl+Z / Ctrl+D 或留空行回车结束）：")
    print("例如：一个蓝色圆形逐渐变成红色方块，中间有缩放和淡入淡出效果。")

    print("\n—— 开始输入描述 ——")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip() and lines:
            # 遇到空行且已有内容，结束输入
            break
        lines.append(line)
    prompt = "\n".join(lines).strip()

    if not prompt:
        print("未输入描述，退出。")
        return

    # 生成 + 多轮修正
    print(f"\n[Step 1] 生成并修正 Manim 代码: {class_name}")
    code = refine_manim_scene(class_name, prompt)

    # 保存到独立文件
    print(f"\n[Step 2] 保存到 generated_scenes/{class_name}.py")
    scene_file = save_scene_to_library(code, class_name)

    # 询问是否渲染
    print("\n[Step 3] 是否立即调用 manim 进行一次测试渲染？")
    choice = input("输入 y 渲染，直接回车跳过: ").strip().lower()
    if choice != "y":
        print("已跳过渲染，仅生成代码。")
        return

    print(f"\n[Step 3] 调用 manim 渲染 {class_name}（质量: -ql 低清预览）")
    cmd = _manim_command("l", scene_file, class_name)
    print("命令:", " ".join(cmd))

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except FileNotFoundError:
        print("\n[错误] 未找到 manim 命令，请确认已在当前环境安装 manim。")
        return
    except subprocess.TimeoutExpired:
        print("\n[错误] 渲染超时 (>300s)。")
        return

    if proc.returncode != 0:
        print("\n[渲染失败] Manim 返回非 0 状态码。")
        err_text = (proc.stderr or proc.stdout or "").strip() or "(no stderr/stdout)"
        print(err_text[-1600:])
        return

    print("\n[渲染成功] Manim 命令执行成功。")
    print("你可以根据项目配置，在 media/videos 下找到生成的视频文件。")


def _infer_project_name(script_path: str) -> str | None:
    """
    根据脚本路径推断项目名：
      - 形如 projects/number2/script.json -> project_name = "number2"
      - 否则返回 None，表示使用默认 generated_scenes 根目录。
    """
    abs_path = os.path.abspath(script_path)
    parts = abs_path.replace("\\", "/").split("/")
    if "projects" in parts:
        idx = parts.index("projects")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None


def batch_from_script(script_path: str, render: bool = False):
    """
    从 script.json 批量为所有 manim 场景生成/修正 Scene 代码，并可选进行低清渲染。
    """
    # 解析脚本
    if not os.path.isabs(script_path):
        script_path = os.path.join(PROJECT_ROOT, script_path)

    project_name = _infer_project_name(script_path)
    if project_name:
        print(f"\n[Script] 使用脚本: {script_path}  (project={project_name})")
        base_dir = os.path.join(PROJECT_ROOT, "visuals", "generated_scenes", project_name)
    else:
        print(f"\n[Script] 使用脚本: {script_path}")
        base_dir = None
    scenes: List[SceneItem] = parse_script(script_path)
    manim_scenes = [s for s in scenes if s.visual_type == "manim" and s.visual_source]

    if not manim_scenes:
        print("脚本中没有 visual.type == 'manim' 的场景。")
        return

    print(f"共 {len(manim_scenes)} 个 manim 场景，将逐个生成/修正代码。")

    for scene in manim_scenes:
        class_name = scene.visual_source
        prompt = scene.visual_prompt or scene.text or ""
        print("\n" + "-" * 60)
        print(f"[Scene] id={scene.id}  class={class_name}")

        if not class_name:
            print("  [跳过] 缺少 scene_class。")
            continue
        if not prompt:
            print("  [跳过] 缺少 prompt/text 描述。")
            continue

        # 生成 + 多轮修正
        print(f"  [Step 1] 生成并修正 Manim 代码: {class_name}")
        code = refine_manim_scene(class_name, prompt)

        # 保存到独立文件（按项目名归档）
        if base_dir:
            print(f"  [Step 2] 保存到 generated_scenes/{project_name}/{class_name}.py")
            scene_file = save_scene_to_library(code, class_name, base_dir=base_dir)
        else:
            print(f"  [Step 2] 保存到 generated_scenes/{class_name}.py")
            scene_file = save_scene_to_library(code, class_name)

        if not render:
            continue

        # 可选：立刻渲染一次
        print(f"  [Step 3] 调用 manim 渲染 {class_name}（质量: -ql 低清预览）")
        cmd = _manim_command("l", scene_file, class_name)
        print("  命令:", " ".join(cmd))

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        except FileNotFoundError:
            print("  [错误] 未找到 manim 命令，请确认已在当前环境安装 manim。")
            return
        except subprocess.TimeoutExpired:
            print("  [错误] 渲染超时 (>300s)。")
            continue

        if proc.returncode != 0:
            print("  [渲染失败] Manim 返回非 0 状态码。")
            err_text = (proc.stderr or proc.stdout or "").strip() or "(no stderr/stdout)"
            print(err_text[-1600:])
            continue

        print("  [渲染成功]")


def main():
    """
    主入口：
      - 如果提供了 script.json 路径，则对脚本中的所有 manim 场景批量生成/修正；
      - 否则进入单 Scene 交互测试模式。
    """
    args = sys.argv[1:]
    if args:
        script_arg = args[0]
        render_flag = "--render" in args[1:]
        batch_from_script(script_arg, render=render_flag)
        print("\n完成 script.json 批量测试。")
        return

    while True:
        interactive_once()
        again = input("\n是否继续测试下一个 Scene？(y 继续 / 其他退出): ").strip().lower()
        if again != "y":
            break

    print("\n完成。")


if __name__ == "__main__":
    main()

