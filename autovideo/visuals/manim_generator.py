"""Manim 代码生成器 - 使用 LLM 自动生成缺失的 Manim 场景代码"""

import os
import sys
from openai import OpenAI

# 添加项目根目录到 sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import load_config

SYSTEM_PROMPT = """You are an expert Manim (Community Edition v0.18+) developer.
Your task is to write a Python class inheriting from `Scene` based on a user description.

CRITICAL RULES (violating ANY of these will cause runtime errors):

=== IMPORTS ===
1. ONLY use `from manim import *`. Do NOT import from submodules like `manim.utils.color`.
2. Colors are directly available as constants: RED, BLUE, GREEN, YELLOW, PURPLE, PURPLE_A, PURPLE_E, GREY_C, TEAL_A, etc.
   - NEVER use `Colors.xxx.value` or `Colors.xxx` - this syntax does NOT exist.

=== FORBIDDEN CLASSES (will cause FileNotFoundError or ImportError) ===
3. NEVER use: SVGMobject, ImageMobject, Tex, MathTex, Sphere, Cube, ThreeDScene, or any 3D objects.
4. NEVER reference external files (svg, png, jpg, etc).

=== ALLOWED PRIMITIVES ONLY ===
5. Use ONLY these built-in 2D shapes:
   - Text, Circle, Ellipse, Rectangle, RoundedRectangle, Square, Triangle, Polygon
   - Line, Arrow, DoubleArrow, Arc, ArcBetweenPoints, CurvedArrow
   - Dot, Annulus, RegularPolygon
   - VGroup, NumberPlane, Axes, FunctionGraph
   - For brain/eye/ear/icon shapes: combine Circle, Ellipse, Arc primitives

=== API CORRECTNESS ===
6. Arrow/DoubleArrow: use positional args `Arrow(start, end)`, NOT `Arrow(start_point=..., end_point=...)`.
7. Text: use `weight=BOLD`, NOT `font_weight=...`.
8. Rate functions: use `rate_func=smooth` or `rate_func=rate_functions.ease_in_out_sine`, NOT bare `ease_in`.
9. Z-index: use `obj.set_z_index(-1)`, NOT `self.add_to_back(obj)`.
10. Chinese text: use `Text("中文", font="Microsoft YaHei")`.

=== CODE STYLE ===
11. Output ONLY Python code. No markdown, no explanations, no ```python blocks.
12. Class name MUST match the requested name exactly.
13. Keep animations 5-10 seconds. Use self.wait() between animations.
14. Black background is default (no need to set).

Example Input:
Class Name: "CircleToSquare"
Description: "A blue circle transforms into a red square."

Example Output:
from manim import *

class CircleToSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)

        self.play(Create(circle))
        self.wait(1)
        self.play(Transform(circle, square))
        self.wait(1)
"""

def generate_manim_code(class_name: str, prompt: str, config_path: str = None) -> str:
    """
    使用 LLM 生成 Manim 代码
    """
    cfg = load_config(config_path)
    client = OpenAI(
        api_key=cfg.llm.api_key,
        base_url=cfg.llm.base_url,
    )
    
    user_content = f"""Class Name: "{class_name}"
Description: "{prompt}"
"""

    print(f"  [Auto-Gen] 正在生成 Manim 代码: {class_name}...")
    
    response = client.chat.completions.create(
        model=cfg.llm.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        # 代码生成更看重稳定性而不是创造性
        temperature=0.2,
    )
    
    code = response.choices[0].message.content.strip()

    # 清理 markdown 标记
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    # 自动修复常见的 LLM 幻觉错误
    code = sanitize_manim_code(code, class_name=class_name)

    return code


def _static_manim_checks(code: str) -> list[str]:
    """
    纯文本静态检查，返回可能导致运行期崩溃的问题列表。
    不修改代码，仅用于驱动后续的 LLM 修正。
    """
    issues: list[str] = []

    patterns = [
        ("SVGMobject", "使用了 SVGMobject，可能依赖外部 SVG 资源"),
        (".svg", "字符串中包含 .svg，可能依赖外部 SVG 文件"),
        (".png", "字符串中包含 .png，可能依赖外部图片文件"),
        (".jpg", "字符串中包含 .jpg，可能依赖外部图片文件"),
        (".jpeg", "字符串中包含 .jpeg，可能依赖外部图片文件"),
        ("Tex(", "使用了 Tex（需要 LaTeX 依赖）"),
        ("MathTex(", "使用了 MathTex（需要 LaTeX 依赖）"),
        ("ImageMobject(", "使用了 ImageMobject（需要外部图片文件）"),
        ("ThreeDScene(", "继承了 ThreeDScene（当前环境不支持 3D）"),
        ("set_camera_orientation(", "调用了 3D 相机接口 set_camera_orientation"),
        ("italic=", "使用了 italic 关键字参数，当前版本可能不支持"),
    ]

    for token, msg in patterns:
        if token in code:
            issues.append(msg)

    return issues


def _llm_fix_manim_code(
    previous_code: str,
    errors: list[str],
    class_name: str,
    config_path: str | None = None,
) -> str:
    """
    在已有代码和错误信息的基础上，请 LLM 做“修正而不是重写”。
    """
    cfg = load_config(config_path)
    client = OpenAI(
        api_key=cfg.llm.api_key,
        base_url=cfg.llm.base_url,
    )

    error_text = "\n".join(f"- {e}" for e in errors) if errors else "（本轮无显式错误，仅做规则收紧和小修正）"

    user_content = f"""You previously wrote a Manim Scene class named {class_name}.
Now fix the code based on the errors and constraints below.

CRITICAL INSTRUCTIONS:
- DO NOT change the class name (must stay exactly {class_name}).
- Prefer minimal edits: keep the overall structure and animation idea.
- Remove or replace any APIs that are not available in Manim CE 0.18+.

Errors and issues to fix:
{error_text}

Current code:
\"\"\"python
{previous_code}
\"\"\""""

    print(f"  [Auto-Gen] 正在根据错误信息修正 Manim 代码: {class_name}...")

    response = client.chat.completions.create(
        model=cfg.llm.model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        temperature=0.1,
    )

    code = response.choices[0].message.content.strip()

    # 清理 markdown 标记
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    return code


def refine_manim_scene(
    class_name: str,
    prompt: str,
    max_rounds: int = 2,
    config_path: str | None = None,
) -> str:
    """
    多轮生成 + 修正 Manim Scene 代码。

    逻辑：
    - 第 1 轮：正常调用 generate_manim_code 生成代码；
    - 对生成结果做 sanitize + 静态检查；
    - 若仍有明显问题，在错误列表基础上调用 LLM 做“修正”，重复最多 max_rounds 轮；
    - 返回最后一版代码（即使还有少量问题，也会把信息打印出来）。
    """
    code: str | None = None
    issues: list[str] = []

    for round_idx in range(max_rounds):
        human_round = round_idx + 1
        if code is None:
            # 第一次完整生成
            print(f"  [Refine] 第 {human_round}/{max_rounds} 轮：生成初始代码 {class_name}")
            code = generate_manim_code(class_name, prompt, config_path=config_path)
        else:
            # 后续轮次在已有代码基础上修正
            print(f"  [Refine] 第 {human_round}/{max_rounds} 轮：根据错误修正 {class_name}")
            code = _llm_fix_manim_code(code, issues, class_name, config_path=config_path)

        # 每一轮都做一次 sanitize，保证基本规则
        code = sanitize_manim_code(code, class_name=class_name)

        # 做静态检查，看还有没有明显违规模式
        issues = _static_manim_checks(code)
        if not issues:
            print(f"  [Refine] 第 {human_round} 轮后通过静态检查: {class_name}")
            break

        print(f"  [Refine] 第 {human_round} 轮后仍发现问题，将尝试进一步修正: {issues}")

    return code


def sanitize_manim_code(code: str, class_name: str | None = None) -> str:
    """
    自动修复 LLM 生成的 Manim 代码中常见的错误
    """
    import re

    fixes_applied = []

    # 0. 确保 import 语句存在
    if "from manim import *" not in code:
        code = "from manim import *\n\n" + code
        fixes_applied.append("added manim import")

    # 0.1 确保 class 名称与期望一致（只修第一个 Scene 子类）
    if class_name is not None:
        class_match = re.search(r"class\s+(\w+)\s*\(\s*Scene\s*\)\s*:", code)
        if class_match:
            real_name = class_match.group(1)
            if real_name != class_name:
                code = re.sub(
                    rf"class\s+{real_name}\s*\(\s*Scene\s*\)\s*:",
                    f"class {class_name}(Scene):",
                    code,
                    count=1,
                )
                fixes_applied.append("normalized class name")
        else:
            # 如果完全没有 Scene 子类，给一个最简单的兜底 Scene，避免直接崩溃
            code = f"""from manim import *

class {class_name}(Scene):
    def construct(self):
        title = Text("Scene generation failed", font="Microsoft YaHei")
        self.add(title)
"""
            fixes_applied.append("added fallback Scene")
            print(f"    [Sanitize] Applied fixes: {', '.join(fixes_applied)}")
            return code

    # 1. 移除错误的 Colors 导入
    if "from manim.utils.color import Colors" in code:
        code = code.replace("from manim.utils.color import Colors", "# Colors are available directly from manim")
        fixes_applied.append("removed Colors import")

    # 2. 替换 Colors.xxx.value 为直接颜色常量
    colors_pattern = r'Colors\.(\w+)\.value'
    def replace_color(match):
        color_name = match.group(1).upper()
        return color_name
    if re.search(colors_pattern, code):
        code = re.sub(colors_pattern, replace_color, code)
        fixes_applied.append("replaced Colors.xxx.value")

    # 3. 替换 Colors.xxx 为直接颜色常量 (不带 .value)
    colors_pattern2 = r'Colors\.(\w+)'
    if re.search(colors_pattern2, code):
        code = re.sub(colors_pattern2, replace_color, code)
        fixes_applied.append("replaced Colors.xxx")

    # 4. 修复 Arrow/DoubleArrow 的 start_point/end_point 参数
    # Arrow(start_point=X, end_point=Y, ...) -> Arrow(X, Y, ...)
    arrow_pattern = r'(Arrow|DoubleArrow)\s*\(\s*start_point\s*=\s*([^,]+),\s*end_point\s*=\s*([^,)]+)'
    def replace_arrow(match):
        arrow_type = match.group(1)
        start = match.group(2).strip()
        end = match.group(3).strip()
        return f'{arrow_type}({start}, {end}'
    if re.search(arrow_pattern, code):
        code = re.sub(arrow_pattern, replace_arrow, code)
        fixes_applied.append("fixed Arrow start_point/end_point")

    # 5. 替换 SVGMobject 为内置形状占位符（带警告注释）
    svg_patterns = [
        (r'SVGMobject\s*\(\s*["\']brain["\']\s*\)[^)]*', '_create_brain_shape()'),
        (r'SVGMobject\s*\(\s*["\']eye["\']\s*\)[^)]*', '_create_eye_shape()'),
        (r'SVGMobject\s*\(\s*["\']ear["\']\s*\)[^)]*', '_create_ear_shape()'),
        (r'SVGMobject\s*\(\s*["\']speech_bubble["\']\s*\)[^)]*', '_create_speech_bubble()'),
        (r'SVGMobject\s*\([^)]+\)[^)]*', 'Circle(radius=0.5, color=GREY)  # TODO: SVG replaced with placeholder'),
    ]
    for pattern, replacement in svg_patterns:
        if re.search(pattern, code):
            code = re.sub(pattern, replacement, code)
            fixes_applied.append(f"replaced SVGMobject")

    # 6. 如果使用了辅助函数，添加它们的定义
    helper_functions = ""
    if '_create_brain_shape()' in code:
        helper_functions += '''
def _create_brain_shape():
    """Create a brain-like shape using built-in primitives"""
    left = Ellipse(width=0.8, height=1.1, fill_color=PURPLE_E, fill_opacity=0.8, stroke_color=PURPLE_A, stroke_width=1)
    right = Ellipse(width=0.8, height=1.1, fill_color=PURPLE_E, fill_opacity=0.8, stroke_color=PURPLE_A, stroke_width=1)
    left.shift(LEFT * 0.25)
    right.shift(RIGHT * 0.25)
    fold1 = Arc(radius=0.3, angle=PI, stroke_color=PURPLE_A, stroke_width=1).shift(UP * 0.15)
    fold2 = Arc(radius=0.25, angle=PI, stroke_color=PURPLE_A, stroke_width=1).shift(DOWN * 0.15).rotate(PI)
    return VGroup(left, right, fold1, fold2)

'''
    if '_create_eye_shape()' in code:
        helper_functions += '''
def _create_eye_shape():
    """Create an eye shape using built-in primitives"""
    white = Circle(radius=0.35, fill_color=WHITE, fill_opacity=0.95, stroke_color=GREY_B, stroke_width=1)
    iris = Circle(radius=0.18, fill_color=BLUE_D, fill_opacity=1, stroke_width=0)
    pupil = Circle(radius=0.07, fill_color=BLACK, fill_opacity=1, stroke_width=0)
    return VGroup(white, iris, pupil)

'''
    if '_create_ear_shape()' in code:
        helper_functions += '''
def _create_ear_shape():
    """Create an ear shape using built-in primitives"""
    outer = Ellipse(width=0.5, height=0.8, fill_color=GREY_C, fill_opacity=0.85, stroke_color=GREY_B, stroke_width=1)
    inner = Arc(radius=0.25, angle=PI*0.7, stroke_color=GREY_B, stroke_width=1).rotate(-PI/4).shift(LEFT * 0.05)
    return VGroup(outer, inner)

'''
    if '_create_speech_bubble()' in code:
        helper_functions += '''
def _create_speech_bubble():
    """Create a speech bubble using built-in primitives"""
    body = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.2, fill_color=WHITE, fill_opacity=0.9, stroke_color=GREY_B, stroke_width=1)
    tail = Triangle(fill_color=WHITE, fill_opacity=0.9, stroke_color=GREY_B, stroke_width=1)
    tail.scale(0.2).rotate(-PI/2).next_to(body, DOWN, buff=-0.05).shift(LEFT * 0.5)
    return VGroup(body, tail)

'''

    # 如果有辅助函数，在 class 定义之前插入
    if helper_functions:
        # 找到 class 定义的位置
        class_match = re.search(r'^class\s+\w+', code, re.MULTILINE)
        if class_match:
            insert_pos = class_match.start()
            code = code[:insert_pos] + helper_functions + code[insert_pos:]
            fixes_applied.append("added helper functions")

    # 7. 修复 font_weight -> weight
    if 'font_weight=' in code:
        code = code.replace('font_weight=', 'weight=')
        fixes_applied.append("fixed font_weight -> weight")

    # 8. 移除 Sphere/Cube 等 3D 对象 (替换为 Circle)
    if 'Sphere(' in code:
        code = re.sub(r'Sphere\s*\([^)]*\)', 'Circle(radius=1, fill_opacity=0.8)', code)
        fixes_applied.append("replaced Sphere with Circle")
    if 'Cube(' in code:
        code = re.sub(r'Cube\s*\([^)]*\)', 'Square(side_length=1, fill_opacity=0.8)', code)
        fixes_applied.append("replaced Cube with Square")

    # 8.1 移除 Text 等对象中不被支持的 italic 参数，避免 TypeError
    # 以及部分版本不支持的 max_tip_length_to_length_ratio / align 等参数
    # 形如 ..., italic=True/False) -> 直接删掉该关键字参数
    italic_pattern = r',\s*italic\s*=\s*(True|False)'
    if re.search(italic_pattern, code):
        code = re.sub(italic_pattern, '', code)
        fixes_applied.append("removed unsupported italic kwarg")

    # 形如 ..., max_tip_length_to_length_ratio=0.2) -> 删除该关键字参数
    max_tip_pattern = r',\s*max_tip_length_to_length_ratio\s*=\s*[^,)]+'
    if re.search(max_tip_pattern, code):
        code = re.sub(max_tip_pattern, '', code)
        fixes_applied.append("removed unsupported max_tip_length_to_length_ratio kwarg")

    # 形如 ..., align="center") -> 删除该关键字参数（部分 VMobject 不支持）
    align_pattern = r',\s*align\s*=\s*[^,)]+'
    if re.search(align_pattern, code):
        code = re.sub(align_pattern, '', code)
        fixes_applied.append("removed unsupported align kwarg")

    # 9. 统一兜底未知 rate_func 为 smooth
    rate_pattern = r"rate_func\s*=\s*([a-zA-Z0-9_\.]+)"

    def replace_rate(match):
        name = match.group(1)
        allowed = {"smooth", "linear", "rate_functions.ease_in_out_sine"}
        if name in allowed:
            return f"rate_func={name}"
        return "rate_func=smooth"

    if re.search(rate_pattern, code):
        code = re.sub(rate_pattern, replace_rate, code)
        fixes_applied.append("normalized rate_func")

    # 9.1 移除 3D 相机接口 set_camera_orientation，避免普通 Scene 上的 AttributeError
    if "set_camera_orientation(" in code:
        code = re.sub(
            r'self\.set_camera_orientation\s*\([^)]*\)',
            '# set_camera_orientation removed (3D API not available on Scene)',
            code,
        )
        fixes_applied.append("removed set_camera_orientation")

    # 10. 简单黑名单扫描：Tex/MathTex/ImageMobject/SVGMobject/ThreeDScene/外部文件
    forbidden_replacements = {
        "Tex(": "Text(",
        "MathTex(": "Text(",
        "ImageMobject(": "Circle(",
        "ThreeDScene(": "Scene(",
    }
    for bad, good in forbidden_replacements.items():
        if bad in code:
            code = code.replace(bad, good)
            fixes_applied.append(f"replaced {bad.strip('(')}")

    # 外部资源文件后缀：直接去掉字符串中的文件名，保留文字
    if any(ext in code for ext in [".svg", ".png", ".jpg", ".jpeg"]):
        code = re.sub(r'["\']([^"\']+\.(svg|png|jpg|jpeg))["\']', '"asset"', code)
        fixes_applied.append("removed external asset filenames")

    if fixes_applied:
        print(f"    [Sanitize] Applied fixes: {', '.join(fixes_applied)}")

    return code


def save_scene_to_library(code: str, class_name: str, base_dir: str | None = None) -> str:
    """
    将生成的 Scene 代码保存为独立文件，便于管理和多轮迭代。

    默认保存到 visuals/generated_scenes/<ClassName>.py
    返回保存后的文件绝对路径。
    """
    if base_dir is None:
        base_dir = os.path.join(os.path.dirname(__file__), "generated_scenes")

    os.makedirs(base_dir, exist_ok=True)

    file_path = os.path.join(base_dir, f"{class_name}.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code.rstrip() + "\n")

    print(f"  [Auto-Gen] 代码已保存到独立文件 {os.path.relpath(file_path, os.path.dirname(__file__))}")
    return file_path

def append_to_manim_scenes(code: str, file_path: str = None):
    """
    将生成的代码追加到 visuals/manim_scenes.py
    """
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "manim_scenes.py")
        
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n\n" + "# " + "="*20 + " Auto-Generated " + "="*20 + "\n")
        f.write(code + "\n")
    
    print(f"  [Auto-Gen] 代码已追加到 {os.path.basename(file_path)}")

if __name__ == "__main__":
    # Test
    code = generate_manim_code("TestScene", "一个三角形旋转并变色")
    print(code)
