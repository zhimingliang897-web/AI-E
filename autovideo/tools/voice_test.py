"""
TTS 声音试听工具 - 支持 edge-tts 和 ChatTTS
用法：python tools/voice_test.py
"""

import asyncio
import os
import subprocess
import sys
import tempfile

# ── 试听文本（可改成你自己的台词）──────────────────────────────
SAMPLE_TEXT = (
    "什么是 Prompt？\n\n"
    "在拥有了超级大脑（LLM）和视觉感知能力之后，AI 并不能自动知晓你的具体意图，它需要一个明确的指令来激活。这个指令，就叫 Prompt，中文通常翻译为“提示词”。它是你输入给模型的一段文字，也是你和 AI 交流的核心桥梁。简单来说，Prompt 就是你对 AI 发出的具体任务指令。\n\n"
    "为什么叫 Prompt？\n"
    "这个词在英语里有“提示、驱使”的含义。\n"
    "我们可以把 AI 想象成一位博学但需要引导的演员，而你则是导演或提词员。\n"
    "如果你不给它明确的提示（Prompt），它可能无法开始工作，或者生成的内容偏离预期。\n"
    "你的任务，就是提供清晰的线索，引导它基于这些线索，通过概率计算，一步步生成符合你要求的内容。\n\n"
    "Prompt 的质量，直接决定了 AI 的输出效果。\n"
    "这在计算机领域遵循一个基本原则：Garbage In, Garbage Out（垃圾进，垃圾出）。\n"
    "大语言模型本质上是一个概率预测工具。Prompt 的作用，就是“限定”这个概率预测的范围和方向。\n"
    "你给的约束越具体，它生成的内容就越精准；你给的指令越模糊，结果就越容易不可控。\n\n"
    "我们来看个对比。"
)

EDGE_VOICES = [
    # ── 中文 (普通话 & 方言) ──
    ("zh-CN-YunxiNeural",   "男 · 小说/故事风   · 最自然，有语气起伏"),
    ("zh-CN-YunyangNeural", "男 · 新闻播报风    · 清晰专业，沉稳"),
    ("zh-CN-YunjianNeural", "男 · 体育/激情风   · 有力，节奏感强"),
    ("zh-CN-XiaoxiaoNeural","女 · 新闻/小说风   · 当前默认，甜但 AI 感强"),
    ("zh-CN-XiaoyiNeural",  "女 · 卡通风        · 活泼轻快"),
    ("zh-CN-YunxiaNeural",  "男 · 卡通/少年风   · 年轻感"),
    ("zh-CN-liaoning-XiaobeiNeural", "女 · 东北方言     · 有亲切感，非普通话"),
    ("zh-CN-shaanxi-XiaoniNeural",   "女 · 陕西方言     · 地方口音"),
    ("zh-TW-HsiaoChenNeural","女 · 台湾腔        · 温柔亲切"),
    ("zh-TW-YunJheNeural",  "男 · 台湾腔        · 沉稳儒雅"),
    ("zh-HK-HiuMaanNeural", "女 · 粤语 (香港)   · 标准粤语播报"),
    ("zh-HK-WanLungNeural", "男 · 粤语 (香港)   · 粤语男声"),
    
    # ── 英文 (英语) ──
    ("en-US-AriaNeural",    "女 · 美式英语      · 沉稳专业，适合新闻/讲解"),
    ("en-US-ChristopherNeural", "男 · 美式英语  · 纪录片旁白风格，低沉有磁性"),
    ("en-US-GuyNeural",     "男 · 美式英语      · 阳光轻松，适合生活类短视频"),
    ("en-US-SteffanNeural", "男 · 美式英语      · 严谨清晰，适合教学演示"),
    ("en-US-JennyNeural",   "女 · 美式英语      · 自然亲切，适用性广"),
    ("en-US-MichelleNeural","女 · 美式英语      · 温暖舒缓，适合解说记录"),
    ("en-US-EricNeural",    "男 · 美式英语      · 浑厚有力"),
    
    ("en-GB-SoniaNeural",   "女 · 英式英语      · 优雅端庄的伦敦音"),
    ("en-GB-RyanNeural",    "男 · 英式英语      · 温暖大气的英式广播腔"),
    ("en-GB-LibbyNeural",   "女 · 英式英语      · 清晰干练"),
    
    ("en-AU-NatashaNeural", "女 · 澳洲英语      · 轻快独特的澳洲口音"),
    ("en-AU-WilliamNeural", "男 · 澳洲英语      · 随性自然的澳洲发音"),
    ("en-CA-ClaraNeural",   "女 · 英语 (加拿大) · 清晰平缓的中性口音"),
    
    # ── 其他常用外语 ──
    ("ja-JP-NanamiNeural",  "女 · 日语          · 年轻活泼，动漫风"),
    ("ja-JP-KeitaNeural",   "男 · 日语          · 清晰沉稳的男声"),
    ("ko-KR-SunHiNeural",   "女 · 韩语          · 甜美韩剧风"),
    ("ko-KR-InJoonNeural",  "男 · 韩语          · 标准成熟男声"),
    ("fr-FR-DeniseNeural",  "女 · 法语          · 优雅正宗的巴黎法语"),
    ("de-DE-KatjaNeural",   "女 · 德语          · 严谨清晰的德语播报"),
]

# ── edge-tts 测试不同语速 ────────────────────────────────────────
EDGE_RATES = [
    ("+0%",  "正常语速"),
    ("-8%",  "慢 8%（推荐）"),
    ("-15%", "慢 15%（较慢）"),
]

# ── ChatTTS 预设种子 ────────────────────────────────────────────
CHATTTS_SEEDS = [
    (2222, "默认种子 · 中性声线"),
    (1234, "随机种子1"),
    (5678, "随机种子2"),
    (9999, "随机种子3"),
    (42,   "随机种子4"),
    (666,  "随机种子5"),
    (8888, "随机种子6"),
    (3141, "随机种子7"),
]

# ── ChatTTS 语速选项 ────────────────────────────────────────────
CHATTTS_SPEEDS = [
    (3, "偏慢 (speed=3)"),
    (4, "推荐 (speed=4，类似真人读稿)"),
    (5, "较快 (speed=5)"),
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "voice_samples")

# ChatTTS 路径
CHATTTS_PATH = r"E:\Ip\免费 ChatTTS自带情感文字转语音工具\ChatTTS_colab_offline"
CHATTTS_PYTHON = os.path.join(CHATTTS_PATH, "runtime", "python.exe")
CHATTTS_MODEL_PATH = os.path.join(CHATTTS_PATH, "models")


def play(path: str):
    """调用系统播放器播放音频"""
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.run(["afplay", path])
    else:
        subprocess.run(["ffplay", "-nodisp", "-autoexit", path],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def menu(title: str, items: list, allow_all=True) -> list:
    """通用选择菜单，返回选中的 index 列表"""
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")
    for i, item in enumerate(items):
        if isinstance(item, tuple) and len(item) == 2:
            key, desc = item
            print(f"  [{i+1}] {key}  —  {desc}")
        else:
            print(f"  [{i+1}] {item}")
    if allow_all:
        print(f"  [0] 全部生成")
    print(f"  [q] 退出")
    print(f"{'─'*50}")

    raw = input("请输入编号（空格分隔多个，如 1 3）: ").strip().lower()
    if raw == "q":
        return None
    if raw == "0" and allow_all:
        return list(range(len(items)))
    chosen = []
    for tok in raw.split():
        try:
            idx = int(tok) - 1
            if 0 <= idx < len(items):
                chosen.append(idx)
        except ValueError:
            pass
    return chosen


def get_test_text() -> str:
    """获取要测试的文本，允许用户输入自己的 txt 文件路径"""
    print(f"\n   [文本选择]")
    print("   直接按 Enter 使用内建默认文本，或者输入你的 .txt 脚本文件路径：")
    txt_path = input("   > ").strip()
    
    if txt_path:
        # 移除两端的引号（防拖拽）
        txt_path = txt_path.strip('"').strip("'")
        if os.path.exists(txt_path):
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if content:
                    print(f"   ✓ 成功加载文件: {txt_path}\n")
                    return content
                else:
                    print("   [警告] 文件为空，回退使用默认文本。\n")
            except Exception as e:
                print(f"   [警告] 读取文件出错 ({e})，回退使用默认文本。\n")
        else:
            # 尝试相对于 autovideo 根目录查找
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            fallback_path = os.path.join(parent_dir, txt_path)
            if os.path.exists(fallback_path):
                try:
                    with open(fallback_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    if content:
                        print(f"   ✓ 成功加载文件: {fallback_path}\n")
                        return content
                    else:
                        print("   [警告] 文件为空，回退使用默认文本。\n")
                except Exception as e:
                    print(f"   [警告] 读取文件出错 ({e})，回退使用默认文本。\n")
            else:
                print(f"   [警告] 找不到文件 {txt_path}，回退使用默认文本。\n")
            
    # 使用默认
    preview = SAMPLE_TEXT[:50].replace('\n', ' ') + "..."
    print(f"   使用内建文本: 「{preview}」\n")
    return SAMPLE_TEXT

# ═══════════════════════════════════════════════════════════════════
#  edge-tts 测试
# ═══════════════════════════════════════════════════════════════════

async def edge_generate(voice: str, rate: str, path: str, text: str):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(path)


def test_edge_tts():
    """edge-tts 声音试听"""
    print("\n🎙  edge-tts 声音试听")
    print(f"   输出目录: {OUTPUT_DIR}")

    # ⓪ 选文本
    test_text = get_test_text()

    # ① 选声音
    voice_idxs = menu("选择要试听的声音", EDGE_VOICES)
    if voice_idxs is None:
        return
    if not voice_idxs:
        print("未选择声音，返回。")
        return

    # ② 选语速
    rate_idxs = menu("选择语速", EDGE_RATES, allow_all=False)
    if rate_idxs is None:
        return
    if not rate_idxs:
        rate_idxs = [0]   # 默认正常语速

    # ③ 生成
    tasks = []
    file_list = []
    for vi in voice_idxs:
        voice, _ = EDGE_VOICES[vi]
        for ri in rate_idxs:
            rate, rate_label = EDGE_RATES[ri]
            rate_tag = rate.replace("%", "").replace("+", "p").replace("-", "m")
            fname = f"edge_{voice}__rate{rate_tag}.mp3"
            path = os.path.join(OUTPUT_DIR, fname)
            tasks.append((voice, rate, path))
            file_list.append((voice, rate_label, path))

    print(f"\n⏳ 正在生成 {len(tasks)} 个音频...\n")

    async def run_all():
        for voice, rate, path in tasks:
            label = f"{voice}  ({rate})"
            print(f"   生成中: {label}")
            await edge_generate(voice, rate, path, test_text)
            print(f"   ✓ 已保存: {os.path.basename(path)}")

    asyncio.run(run_all())

    # ④ 逐个播放
    play_files(file_list, label_func=lambda v, r, p: f"{v}  [{r}]")


# ═══════════════════════════════════════════════════════════════════
#  ChatTTS 测试 (使用子进程调用，避免依赖冲突)
# ═══════════════════════════════════════════════════════════════════

def chattts_generate_subprocess(seed: int, speed: int, text: str, output_path: str, oral: int, laugh: int, break_: int, padding: float) -> bool:
    """
    通过子进程调用 ChatTTS 离线包的 Python 环境。
    避免 transformers 版本冲突。
    """
    refine_prompt = f"[oral_{oral}][laugh_{laugh}][break_{break_}]"

    # 转义文本中的特殊字符
    escaped_text = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

    script_content = f'''# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"{CHATTTS_PATH}")

from tts_model import load_chat_tts_model, generate_audio_for_seed
from utils import split_text
import shutil
import os

text = """{text}"""
output_path = r"{output_path}"
seed = {seed}
speed = {speed}
refine_prompt = "{refine_prompt}"

print("Loading model...")
chat = load_chat_tts_model(source="local", local_path=r"{CHATTTS_MODEL_PATH}")
print("Model loaded.")

texts = split_text(text, min_length=50)
print(f"Generating {{len(texts)}} segments...")

wav_path = generate_audio_for_seed(
    chat=chat,
    seed=seed,
    texts=texts,
    batch_size=1,
    speed=speed,
    refine_text_prompt=refine_prompt,
)

if wav_path and os.path.exists(wav_path):
    target_wav = wav_path
    
    # 1. 尝试使用 ffmpeg 降噪
    tmp_clean = wav_path + "_clean.wav"
    try:
        import subprocess
        denoise_cmd = [
            "ffmpeg", "-y", "-i", wav_path,
            "-af", "afftdn=nf=-25",
            "-c:a", "pcm_s16le", tmp_clean
        ]
        subprocess.run(denoise_cmd, capture_output=True, check=True)
        if os.path.exists(tmp_clean):
            target_wav = tmp_clean
    except Exception:
        pass

    # 2. 读取音频并追加 padding
    try:
        import wave
        with wave.open(target_wav, 'rb') as w:
            n_channels = w.getnchannels()
            sampwidth = w.getsampwidth()
            framerate = w.getframerate()
            frames = w.readframes(w.getnframes())

        padding = {padding}
        if padding > 0:
            import struct
            fmt = "<" + str(n_channels * sampwidth) + "b"
            zero_frames = struct.pack(fmt, *([0] * (n_channels * sampwidth)))
            silence = zero_frames * int(framerate * padding)
            frames += silence

        with wave.open(output_path, 'wb') as w:
            w.setnchannels(n_channels)
            w.setsampwidth(sampwidth)
            w.setframerate(framerate)
            w.writeframes(frames)
            
        print("SUCCESS")
    except Exception as e:
        import shutil
        shutil.move(wav_path, output_path)
        print("SUCCESS")
        
    # 清理临时文件
    if os.path.exists(tmp_clean):
        try:
            os.remove(tmp_clean)
        except:
            pass
else:
    print("FAILED")
'''

    # 写入临时脚本
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(script_content)
        script_path = f.name

    try:
        print(f"   调用 ChatTTS 子进程...")
        result = subprocess.run(
            [CHATTTS_PYTHON, script_path],
            capture_output=True,
            text=True,
            cwd=CHATTTS_PATH,
            timeout=180,  # 3分钟超时（首次加载模型较慢）
        )

        # 显示进度
        for line in result.stdout.split('\n'):
            if line.strip() and line.strip() not in ['SUCCESS', 'FAILED']:
                print(f"   {line.strip()}")

        if "SUCCESS" in result.stdout:
            return True
        else:
            if result.stderr:
                print(f"   错误: {result.stderr[:300]}")
            return False

    except subprocess.TimeoutExpired:
        print("   超时！")
        return False
    except Exception as e:
        print(f"   执行错误: {e}")
        return False
    finally:
        try:
            os.unlink(script_path)
        except:
            pass


def test_chattts():
    """ChatTTS 声音试听"""
    print("\n🎙  ChatTTS 声音试听")
    print(f"   输出目录: {OUTPUT_DIR}")
    print("\n   💡 提示: seed 决定音色，换不同数字试不同声音")
    print("   ⚠️  首次加载模型较慢，请耐心等待")

    # ⓪ 选文本
    test_text = get_test_text()

    # 选择模式
    mode_items = [
        ("预设种子", "从预设列表选择"),
        ("自定义种子", "输入你想试的种子数字"),
    ]
    mode_idx = menu("选择测试模式", mode_items, allow_all=False)
    if mode_idx is None:
        return

    seeds_to_test = []

    if not mode_idx or mode_idx[0] == 0:
        # 预设种子
        seed_idxs = menu("选择要试听的种子", CHATTTS_SEEDS)
        if seed_idxs is None:
            return
        if not seed_idxs:
            print("未选择种子，返回。")
            return
        seeds_to_test = [(CHATTTS_SEEDS[i][0], f"预设种子 {CHATTTS_SEEDS[i][0]}") for i in seed_idxs]
    else:
        # 自定义种子
        print("\n输入种子数字（空格分隔多个，如: 1234 5678 9999）")
        raw = input("> ").strip()
        if not raw:
            print("未输入种子，返回。")
            return
        for tok in raw.split():
            try:
                s = int(tok)
                seeds_to_test.append((s, f"自定义种子 {s}"))
            except ValueError:
                pass
        if not seeds_to_test:
            print("无效输入，返回。")
            return

    # 自定义语速和情感参数
    print("\n   [自定义参数] (直接按 Enter 使用推荐值)")
    
    speed_input = input("   - speed (语速 1-9, 推荐: 4): ").strip()
    speed = int(speed_input) if speed_input.isdigit() else 4
    
    oral_input = input("   - oral  (口语化 0-9, 推荐: 3): ").strip()
    oral = int(oral_input) if oral_input.isdigit() else 3
    
    laugh_input = input("   - laugh (笑声 0-2, 推荐: 1): ").strip()
    laugh = int(laugh_input) if laugh_input.isdigit() else 1
    
    break_input = input("   - break (停顿 0-7, 推荐: 5): ").strip()
    break_ = int(break_input) if break_input.isdigit() else 5
    
    pad_input = input("   - padding (句末静音秒数, 推荐: 0.3): ").strip()
    try:
        padding = float(pad_input) if pad_input else 0.3
    except:
        padding = 0.3

    # 生成
    file_list = []
    total = len(seeds_to_test)
    print(f"\n⏳ 准备生成 {total} 个音频...\n")

    for seed, seed_label in seeds_to_test:
        fname = f"chattts_seed{seed}_speed{speed}_{int(padding*1000)}ms.wav"
        path = os.path.join(OUTPUT_DIR, fname)

        print(f"   生成中: seed={seed}, speed={speed}, oral={oral}, laugh={laugh}, break={break_}")
        try:
            if chattts_generate_subprocess(seed, speed, test_text, path, oral, laugh, break_, padding):
                print(f"   ✓ 已保存: {fname}")
                file_list.append((seed, f"speed={speed} pad={padding}s", path))
            else:
                print(f"   ✗ 生成失败")
        except Exception as e:
            print(f"   ✗ 错误: {e}")

    if not file_list:
        print("\n没有生成成功的音频。")
        return

    # 播放
    play_files(file_list, label_func=lambda s, sp, p: f"seed={s}  [{sp}]")


# ═══════════════════════════════════════════════════════════════════
#  通用播放
# ═══════════════════════════════════════════════════════════════════

def play_files(file_list, label_func):
    """逐个播放文件"""
    print(f"\n{'─'*50}")
    print("  播放模式（每个播完后按 Enter 继续）")
    print(f"{'─'*50}\n")

    for item in file_list:
        label = label_func(*item)
        path = item[-1]
        print(f"▶  {label}")
        inp = input("   按 Enter 播放，输入 s 跳过: ").strip().lower()
        if inp != "s":
            play(path)
            input("   （播放中...按 Enter 继续下一个）")

    print(f"\n✅ 完成！所有文件保存在:\n   {OUTPUT_DIR}\n")


# ═══════════════════════════════════════════════════════════════════
#  主菜单
# ═══════════════════════════════════════════════════════════════════

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    while True:
        print("\n" + "═"*50)
        print("  🎙  TTS 声音试听工具")
        print("═"*50)
        print("  [1] edge-tts  —  微软云端语音（免费，多种声音）")
        print("  [2] ChatTTS   —  本地模型（自然，可调种子）")
        print("  [q] 退出")
        print("─"*50)

        choice = input("选择 TTS 引擎: ").strip().lower()

        if choice == "1":
            test_edge_tts()
        elif choice == "2":
            test_chattts()
        elif choice == "q":
            print("\n再见！\n")
            break
        else:
            print("无效选择，请重试。")


if __name__ == "__main__":
    main()
