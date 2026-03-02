"""
AutoVideo Pipeline v2 - 两阶段自动化视频生产 (Enhanced Director Mode)

用法:
  # Phase 1: LLM 导演生成脚本 (新增导演控制参数)
  python pipeline.py plan --text scripts/number1.txt --style "Cyberpunk, Neon" --layout "pip_br"
  python pipeline.py plan --text scripts/number1.txt --instruction "多用隐喻，开头要震撼"

  # Phase 2: 合成视频
  python pipeline.py build --script scripts/number1.json
"""

import argparse
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from rich.console import Console
from rich.panel import Panel

from config import load_config, set_project_dir
from parser.script_parser import parse_script
from parser.script_converter import convert_text_to_json
from audio.tts_engine import run_tts
from audio.rvc_engine import convert_with_rvc
from visuals.image_gen import generate_images
from visuals.manim_renderer import render_manim_scenes
from compositor.assembler import assemble_video
from subtitles.srt_generator import generate_srt

import io, sys
console = Console(file=io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace"))


# ===== Phase 1: plan (已重构：增加导演意图注入) =====

def run_plan(args):
    """Phase 1: 用 LLM 导演生成脚本 + 需求清单"""
    start_time = time.time()
    config_path = args.config if args.config else None
    cfg = load_config(config_path)

    console.print(Panel("[bold cyan]AutoVideo Plan - LLM 导演模式 (Enhanced)[/bold cyan]", expand=False))

    if not cfg.llm.enabled and not cfg.llm.api_key:
        console.print("[bold red]错误: LLM 未配置。请在 config.yaml 中设置 llm 段[/bold red]")
        return

    # 3. 处理 Project 路径
    if args.project:
        set_project_dir(cfg, args.project)
        console.print(f"  [Project] 切换到项目目录: {args.project}")

    # 4. 读取文案
    text_path = args.text
    if not os.path.isabs(text_path):
        # 如果有 project，尝试在 project 下找
        if args.project:
            p_text = os.path.join(args.project, text_path)
            if os.path.exists(p_text):
                text_path = p_text
            else:
                text_path = os.path.join(BASE_DIR, text_path)
        else:
            text_path = os.path.join(BASE_DIR, text_path)

    if not os.path.exists(text_path):
        console.print(f"[bold red]文案文件不存在: {text_path}[/bold red]")
        return

    with open(text_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # 5. 注入导演意图 (Prompt Injection)
    # 我们不直接传原文，而是包装一层 Prompt，强制 LLM 改变行为
    director_notes = []
    if args.style:
        director_notes.append(f"- Visual Style (画面风格): {args.style}")
    if args.layout:
        director_notes.append(f"- Default Avatar Layout (默认人像位置): {args.layout} (除非强调画面冲击力，否则默认保持此位置)")
    else:
        # 默认建议：为了避免你讨厌的 fullscreen，我们默认建议用右下角
        director_notes.append("- Default Avatar Layout: pip_br (Picture-in-Picture Bottom Right)")
    if getattr(args, "domain", "auto") != "auto":
        director_notes.append(
            f"- Topic Domain: {args.domain} (Keep examples, metaphors and visual style in this domain)"
        )
    if getattr(args, "lang", "auto") != "auto":
        director_notes.append(
            f"- Output Language: {args.lang} (Generate narration text strictly in this language)"
        )
    
    if args.instruction:
        director_notes.append(f"- Special Instruction (特殊指令): {args.instruction}")

    director_mode = getattr(args, "director", "standard")
    visual_mode = getattr(args, "mode", "image")

    if director_mode == "concept":
        director_notes.append("- Director Mode (导演风格): Concept/Educational. Use split_screen layout often, strongly distill conceptual keywords, and construct a logical flow using manim and solid_bg.")
    elif director_mode == "narrative":
        director_notes.append("- Director Mode (导演风格): Narrative/Passionate. Fast pacing, frequent visual switches, leverage full-screen ai_image for high emotional and visual impact.")
    elif director_mode == "cinematic":
        director_notes.append(
            "- Director Mode (导演风格): Cinematic/Immersive. "
            "Place the 2 ai_video slots at whichever scenes have the strongest visual impact — "
            "could be opening, climax, transition, or any moment where motion adds the most value. "
            "Prefer fullscreen or hidden avatar. All visual prompts should be film-quality cinematography descriptions."
        )

    if visual_mode == "video":
        director_notes.append(
            "- Visual Mode (素材模式): VIDEO mode enabled. "
            "You MAY use ai_video type (max 2 per video) for the most impactful scenes. "
            "ai_video source will be provided by user after generation. "
            "Always provide a fallback field for ai_video scenes using format: \"ai_image::English prompt, cinematic lighting, 4k\""
        )

    # 构造“增强版”文本输入
    # 技巧：通过在文本前加 [DIRECTOR_NOTES]，让下游的 convert_text_to_json 里的 LLM 看到这些要求
    if director_notes:
        augmented_text = (
            "【特殊导演要求】\n"
            "在处理以下文案切分时，请务必将其考虑在内：\n" +
            "\n".join(director_notes) +
            "\n\n『文案正文开始』\n" +
            raw_text +
            "\n『文案正文结束』"
        )
        console.print(Panel("\n".join(director_notes), title="[bold yellow]导演手记注入[/bold yellow]", border_style="yellow"))
    else:
        augmented_text = raw_text

    console.print(f"  [文案] 源文件: {text_path} ({len(raw_text)} 字)")

    # 6. 处理 Avatar 路径
    has_avatar = bool(args.avatar)
    if has_avatar:
        console.print(f"  [Avatar] 视频素材: {args.avatar}")

    # 7. 确定输出路径
    output_path = args.output
    if not output_path:
        # 根据语言参数动态决定文件名
        lang_suffix = getattr(args, "lang", "auto")
        if lang_suffix in ["zh", "en"]:
            fname = f"script_{lang_suffix}.json"
        else:
            fname = "script.json"
        
        if args.project:
            # 项目模式: projects/xxx/script.json 或 script_en.json
            output_path = os.path.join(cfg.paths.scripts, fname)
        else:
            # 兼容模式: scripts/xxx.json
            base = os.path.splitext(os.path.basename(text_path))[0]
            output_path = os.path.join(BASE_DIR, "scripts", f"{base}.json")

    # 8. 调用 LLM (传入增强后的文本)
    console.print("\n  [LLM] 正在构思分镜脚本...")
    
    # 注意：这里我们传入 augmented_text 给转换器
    # 大多数 LLM 在处理 "指令 + 文本" 格式时，会优先遵循指令
    result = convert_text_to_json(
        text=augmented_text,
        output_path=output_path,
        config_path=config_path,
        has_avatar=has_avatar,
        target_lang=getattr(args, "lang", "auto"),
        visual_mode=visual_mode,
    )

    # 9. 保存 Avatar 信息
    if has_avatar:
        avatar_info_path = output_path.replace(".json", "_avatar_info.json")
        import json
        avatar_info = {
            "video_path": os.path.abspath(args.avatar),
            "audio_path": os.path.abspath(args.audio) if args.audio else "",
        }
        with open(avatar_info_path, "w", encoding="utf-8") as f:
            json.dump(avatar_info, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - start_time
    
    # 构建下一步提示
    next_cmd = f"python pipeline.py build"
    if args.project:
        next_cmd += f" --project {args.project}"
    else:
        next_cmd += f" --script {output_path}"

    needs_path = output_path.replace(".json", "_needs.json")
    needs_hint = f"需求清单: {needs_path}" if os.path.exists(needs_path) else ""
    video_hint = ""
    if visual_mode == "video":
        video_hint = ""
    if visual_mode == "video":
        video_hint = "[bold yellow]VIDEO 模式[/bold yellow]: 请按 needs.json 生成 AI 视频，放入 assets/videos/ 后再 build"
    plan_lines = [
        "[bold green]Plan 完成![/bold green]",
        f"脚本: {output_path}",
        f"素材模式: {visual_mode.upper()}",
        f"风格: {args.style if args.style else 'Default'}",
        f"语言: {getattr(args, 'lang', 'auto')}",
        f"耗时: {elapsed:.1f}s",
    ]
    if needs_hint:
        plan_lines.append(needs_hint)
    plan_lines.extend(["", f"下一步:  {next_cmd}"])
    if video_hint:
        plan_lines.append(video_hint)
    plan_text = "\n".join(plan_lines)
    console.print(Panel(plan_text, expand=False))

# ===== Phase 2: build (保持不变) =====

def run_build(args):
    """Phase 2: 完整 pipeline 合成视频"""
    start_time = time.time()
    config_path = args.config if args.config else None
    cfg = load_config(config_path)

    console.print(Panel("[bold cyan]AutoVideo Build Pipeline[/bold cyan]", expand=False))

    # 处理 Project 路径
    if args.project:
        set_project_dir(cfg, args.project)
        console.print(f"  [Project] 切换到项目目录: {args.project}")

    # Cliff 覆盖
    if args.skip_tts:
        cfg.tts.enabled = False
    if args.skip_rvc:
        cfg.rvc.enabled = False
    if args.skip_images:
        cfg.image_gen.enabled = False

    if getattr(args, "lang", None) == "en":
        # Override TTS voice to an English native speaker
        cfg.tts.voice = "en-US-AriaNeural"
        console.print(f"  [Lang] 指定英文生成，自动切换 TTS 发音人为: [yellow]{cfg.tts.voice}[/yellow]")
    elif getattr(args, "lang", None) == "zh":
        cfg.tts.voice = "zh-CN-XiaoxiaoNeural"
        console.print(f"  [Lang] 指定中文生成，自动切换 TTS 发音人为: [yellow]{cfg.tts.voice}[/yellow]")

    # === Step 1: 解析脚本 ===
    console.print("[1/7] [解析] 解析脚本...")

    script_path = args.script
    
    # 如果没指定 script 但指定了 project，我们根据 --lang 寻找对应的脚本
    if not script_path and args.project:
        lang_suffix = getattr(args, "lang", None)
        if lang_suffix in ["zh", "en"]:
            target_fname = f"script_{lang_suffix}.json"
        else:
            target_fname = "script.json"
            
        script_path = os.path.join(cfg.paths.scripts, target_fname)
        
        # 如果带有语言后缀的脚本不存在，作为一个 fallback 回退到默认的 script.json
        if not os.path.exists(script_path) and lang_suffix:
            fallback_path = os.path.join(cfg.paths.scripts, "script.json")
            if os.path.exists(fallback_path):
                console.print(f"  [Lang] 未找到 {target_fname}，回退使用默认 script.json")
                script_path = fallback_path
    
    if not script_path:
        console.print("[bold red]错误: 必须指定 --script 或 --project[/bold red]")
        return

    if not os.path.isabs(script_path):
        script_path = os.path.join(BASE_DIR, script_path)
    if not os.path.exists(script_path):
        # 再次尝试直接路径
        if args.script and os.path.exists(args.script):
            script_path = args.script
        else:
             print(f"[bold red]脚本不存在: {script_path}[/bold red]")
             return

    scenes = parse_script(script_path)

    # 统计
    avatar_count = sum(1 for s in scenes if s.avatar_mode != "hidden")
    auto_audio = sum(1 for s in scenes if s.audio_mode == "auto")
    avatar_audio = sum(1 for s in scenes if s.audio_mode == "avatar")
    console.print(f"  [ok] {len(scenes)} 个场景 (avatar={avatar_count}, auto_audio={auto_audio}, avatar_audio={avatar_audio})")

    if args.only == "parse":
        return

    # === Step 2: Avatar 切割 ===
    console.print("\n[2/7] [Avatar] Avatar 切割...")

    # 检查是否有 avatar 信息
    avatar_info_path = script_path.replace(".json", "_avatar_info.json")
    avatar_video = cfg.avatar.video_path
    avatar_audio_path = cfg.avatar.audio_path

    if os.path.exists(avatar_info_path):
        import json
        with open(avatar_info_path, "r", encoding="utf-8") as f:
            avatar_info = json.load(f)
        avatar_video = avatar_info.get("video_path", avatar_video)
        avatar_audio_path = avatar_info.get("audio_path", avatar_audio_path)

    if avatar_count > 0 and avatar_video and os.path.exists(avatar_video):
        from avatar.splitter import split_avatar_video
        avatar_dir = os.path.join(cfg.paths.assets, "avatar")
        split_avatar_video(
            avatar_video_path=avatar_video,
            avatar_audio_path=avatar_audio_path if avatar_audio_path else None,
            scenes=scenes,
            assets_dir=cfg.paths.assets,
            output_dir=avatar_dir,
        )
        console.print("  [ok] Avatar 切割完成")
    elif avatar_count > 0:
        console.print("  [!]  脚本包含 avatar 场景但未找到 avatar 视频")
    else:
        console.print("  [-]  无 avatar 场景")

    if args.only == "avatar":
        return

    # === Step 3: TTS 配音 ===
    console.print("\n[3/7] [TTS]  TTS 配音...")
    if cfg.tts.enabled:
        audio_dir = os.path.join(cfg.paths.assets, "audio")
        tts_provider = getattr(cfg.tts, "provider", "edge")

        if tts_provider == "chattts":
            # 使用 ChatTTS 本地模型
            from audio.chattts_engine import run_chattts
            console.print(f"  [引擎] ChatTTS (seed={cfg.tts.seed})")
            run_chattts(
                scenes, audio_dir,
                seed=cfg.tts.seed,
                speed=cfg.tts.speed,
                oral=cfg.tts.oral,
                laugh=cfg.tts.laugh,
                break_=cfg.tts.break_,
            )
        else:
            # 默认使用 edge-tts
            console.print(f"  [引擎] edge-tts ({cfg.tts.voice})")
            run_tts(
                scenes, audio_dir,
                voice=cfg.tts.voice,
                rate=cfg.tts.rate,
                pitch=cfg.tts.pitch,
            )
        console.print("  [ok] TTS 完成")
    else:
        console.print("  [-]  已禁用")

    if args.only == "tts":
        return

    # === Step 4: RVC 变声 ===
    console.print("\n[4/7] [RVC] RVC 变声...")
    if cfg.rvc.enabled:
        audio_dir = os.path.join(cfg.paths.assets, "audio")
        rvc_dir = os.path.join(cfg.paths.assets, "audio_rvc")
        convert_with_rvc(
            scenes, audio_dir, rvc_dir,
            api_url=cfg.rvc.api_url,
            model_name=cfg.rvc.model_name,
        )
        console.print("  [ok] RVC 完成")
    else:
        console.print("  [-]  已禁用")

    if args.only == "rvc":
        return

    # === Step 5: Manim 渲染 ===
    console.print("\n[5/7] [Manim] Manim 渲染...")
    if cfg.manim.enabled:
        manim_dir = os.path.join(cfg.paths.assets, "manim")
        render_manim_scenes(
            scenes,
            manim_dir,
            quality=cfg.manim.quality,
            project_name=os.path.basename(os.path.abspath(args.project)) if args.project else None,
        )
        console.print("  [ok] Manim 完成")
    else:
        console.print("  [-]  已禁用")

    if args.only == "manim":
        return

    # === Step 6: AI 图片生成 ===
    console.print("\n[6/7] [生图]  AI 生图...")
    if cfg.image_gen.enabled:
        images_dir = os.path.join(cfg.paths.assets, "images")
        generate_images(
            scenes, images_dir,
            api_key=cfg.image_gen.api_key,
            base_url=cfg.image_gen.base_url,
            model=cfg.image_gen.model,
            max_calls=cfg.image_gen.max_calls,
        )
        console.print("  [ok] 生图完成")
    else:
        console.print("  [-]  已禁用")

    if args.only == "images":
        return

    # === Step 7: 合成视频 ===
    console.print("\n[7/7] [合成]  合成视频...")
    
    # 确定输出文件名
    if args.project:
        out_name = os.path.basename(os.path.abspath(args.project))
    else:
        out_name = os.path.splitext(os.path.basename(script_path))[0]
        
    output_path = os.path.join(cfg.paths.output, f"{out_name}.mp4")
    srt_path = os.path.join(cfg.paths.output, f"{out_name}.srt")

    # 传递字幕和 avatar 配置
    subtitle_cfg = {
        "enabled": cfg.subtitle.enabled,
        "font": cfg.subtitle.font,
        "font_size": cfg.subtitle.font_size,
        "title_font_size": cfg.subtitle.title_font_size,
        "color": cfg.subtitle.color,
        "bg_color": cfg.subtitle.bg_color,
        "bg_opacity": cfg.subtitle.bg_opacity,
    }
    avatar_cfg = {
        "margin": cfg.avatar.margin,
    }
    visual_cfg = {
        "image_motion": cfg.visual.image_motion,
        "ken_burns_zoom": cfg.visual.ken_burns_zoom,
        "ken_burns_pan": cfg.visual.ken_burns_pan,
        "ken_burns_pre_scale": cfg.visual.ken_burns_pre_scale,
        "ken_burns_directions": cfg.visual.ken_burns_directions,
    }

    result = assemble_video(
        scenes,
        assets_dir=cfg.paths.assets,
        output_path=output_path,
        width=cfg.video.width,
        height=cfg.video.height,
        fps=cfg.video.fps,
        codec=cfg.video.codec,
        subtitle_cfg=subtitle_cfg,
        avatar_cfg=avatar_cfg,
        visual_cfg=visual_cfg,
        transition=cfg.video.transition,
        transition_duration=cfg.video.transition_duration,
        default_duration=cfg.video.default_duration,
    )

    if result:
        console.print(f"\n  [ok] 视频输出: {output_path}")

        # 生成外挂字幕（保留 SRT）
        generate_srt(scenes, cfg.paths.assets, srt_path)

        elapsed = time.time() - start_time
        console.print(
            Panel(
                f"[bold green]Pipeline 完成![/bold green]\n"
                f"视频: {output_path}\n"
                f"字幕: {srt_path}\n"
                f"耗时: {elapsed:.1f}s",
                expand=False,
            )
        )
    else:
        console.print("[bold red]合成失败[/bold red]")


def main():
    parser = argparse.ArgumentParser(description="AutoVideo Pipeline v2")
    subparsers = parser.add_subparsers(dest="command")

    # === plan 子命令 (新增参数) ===
    plan_parser = subparsers.add_parser("plan", help="Phase 1: LLM 导演生成脚本")
    plan_parser.add_argument("--project", help="项目目录 (例如: projects/Video01，所有素材输出都在此目录下)")
    plan_parser.add_argument("--text", required=True, help="文案 TXT 文件路径 (支持相对项目路径)")
    plan_parser.add_argument("--avatar", help="Avatar 视频路径")
    plan_parser.add_argument("--audio", help="Avatar 音频路径")
    plan_parser.add_argument("-o", "--output", help="输出 JSON 路径")
    plan_parser.add_argument("--config", help="配置文件路径")
    
    # 新增导演控制参数
    plan_parser.add_argument("--style", help="指定画面风格 (例如: Cyberpunk, Anime, Minimalist)")
    plan_parser.add_argument("--layout", help="指定默认人像位置 (例如: pip_br, hidden, fullscreen)", default="pip_br")
    plan_parser.add_argument(
        "--domain",
        default="auto",
        choices=["auto", "tech", "business", "science", "education", "health", "history", "law", "lifestyle"],
        help="指定话题领域，提升跨主题分镜与视觉一致性",
    )
    plan_parser.add_argument(
        "--lang",
        default="auto",
        choices=["auto", "zh", "en"],
        help="指定输出脚本语言（auto/zh/en）",
    )
    plan_parser.add_argument("--instruction", help="给 LLM 的额外特殊指令 (例如: '开头要有反转', '多用具体例子')")
    plan_parser.add_argument(
        "--director",
        default="standard",
        choices=["standard", "concept", "narrative", "cinematic"],
        help="指定自动导演模式：standard(默认), concept(概念科普), narrative(激情叙事), cinematic(电影沉浸，需 --mode video)",
    )
    plan_parser.add_argument(
        "--mode",
        default="image",
        choices=["image", "video"],
        help="视觉素材模式：image(默认，仅图片) / video(可使用 ai_video，最多2个，需手动放置生成的视频)",
    )

    # === build 子命令 ===
    build_parser = subparsers.add_parser("build", help="Phase 2: 合成视频")
    build_parser.add_argument("--project", help="项目目录 (例如: projects/Video01)")
    build_parser.add_argument("--script", help="脚本 JSON 路径 (默认: {project}/script.json)")
    build_parser.add_argument("--config", help="配置文件路径")
    build_parser.add_argument(
        "--lang",
        choices=["zh", "en"],
        help="覆盖声音语言配置 (en: 自动用英文母语TTS; zh: 自动用中文女生)",
    )
    build_parser.add_argument("--only", choices=["parse", "avatar", "tts", "rvc", "manim", "images", "compose"],
                              help="只运行指定步骤")
    build_parser.add_argument("--skip-tts", action="store_true", help="跳过 TTS")
    build_parser.add_argument("--skip-rvc", action="store_true", help="跳过 RVC")
    build_parser.add_argument("--skip-manim", action="store_true", help="跳过 Manim")
    build_parser.add_argument("--skip-images", action="store_true", help="跳过 AI 生图")

    # === 向后兼容：不带子命令 = build ===
    parser.add_argument("--script", help="脚本 JSON 路径（向后兼容，等同 build --script）")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--only", choices=["parse", "avatar", "tts", "rvc", "manim", "images", "compose"])
    parser.add_argument("--skip-tts", action="store_true")
    parser.add_argument("--skip-rvc", action="store_true")
    parser.add_argument("--skip-manim", action="store_true")
    parser.add_argument("--skip-images", action="store_true")

    args = parser.parse_args()

    if args.command == "plan":
        run_plan(args)
    elif args.command == "build":
        run_build(args)
    elif args.script:
        # 向后兼容：没有子命令但有 --script
        run_build(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
