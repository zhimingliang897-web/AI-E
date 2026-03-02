#!/usr/bin/env python3
"""
download_fonts.py - 无需 sudo，自动搞定 CJK 字体

策略（按顺序）：
  1. assets/fonts/ 已有字体 → 直接用
  2. 系统已装 CJK 字体（/usr/share/fonts 等）→ 软链/复制过来
  3. 以上都没有 → 用 urllib 下载 WQY MicroHei 到 assets/fonts/

用法：
  python scripts/download_fonts.py
"""

import glob
import os
import shutil
import sys
import urllib.request

# ── 路径 ────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
FONTS_DIR    = os.path.join(PROJECT_ROOT, "assets", "fonts")
TARGET_NAME  = "wqy-microhei.ttc"   # 最终放在 assets/fonts/ 下的文件名
TARGET_PATH  = os.path.join(FONTS_DIR, TARGET_NAME)

# WQY MicroHei（文泉驿微米黑）：开源 CJK 字体，约 4.6 MB
FONT_URL = (
    "https://github.com/anthonyfok/fonts-wqy-microhei"
    "/raw/master/wqy-microhei.ttc"
)

# 搜索系统字体时的关键词
CJK_KEYWORDS  = ("cjk", "wqy", "hans", "hant", "chinese", "zh-",
                  "songti", "heiti", "kaiti", "fangzheng", "simsun", "simhei")
# 这些关键词出现时直接跳过（emoji / color bitmap 字体，PIL 无法渲染文字）
EXCLUDE_KEYWORDS = ("emoji", "color", "notocolor", "seguiemj", "symbol",
                    "webdings", "wingdings")
FONT_EXTS    = ("*.ttc", "*.ttf", "*.otf")
SYSTEM_DIRS  = [
    "/usr/share/fonts",
    "/usr/local/share/fonts",
    os.path.expanduser("~/.fonts"),
    os.path.expanduser("~/.local/share/fonts"),
]


def log(msg: str):
    print(f"[fonts] {msg}")


def ensure_dir():
    os.makedirs(FONTS_DIR, exist_ok=True)


def _is_cjk(path: str) -> bool:
    low = os.path.basename(path).lower()
    if any(e in low for e in EXCLUDE_KEYWORDS):
        return False
    return any(k in low for k in CJK_KEYWORDS)


def already_have() -> str:
    """assets/fonts/ 下是否已有 CJK 字体？返回路径或空串"""
    for ext in FONT_EXTS:
        for f in glob.glob(os.path.join(FONTS_DIR, ext)):
            if _is_cjk(f):
                return f
    return ""


def find_system_font() -> str:
    """在系统字体目录里递归搜索 CJK 字体，返回路径或空串（排除 emoji 字体）"""
    for d in SYSTEM_DIRS:
        if not os.path.isdir(d):
            continue
        for ext in FONT_EXTS:
            for f in glob.glob(os.path.join(d, "**", ext), recursive=True):
                if _is_cjk(f):
                    return f
    return ""


def copy_system_font(src: str) -> str:
    """把系统字体复制到 assets/fonts/，返回目标路径"""
    dst = os.path.join(FONTS_DIR, os.path.basename(src))
    if os.path.exists(dst):
        log(f"已存在，跳过复制：{dst}")
        return dst
    log(f"复制系统字体：{src} → {dst}")
    shutil.copy2(src, dst)
    return dst


def download_font() -> str:
    """下载 WQY MicroHei 到 assets/fonts/，返回目标路径"""
    if os.path.exists(TARGET_PATH):
        log(f"已存在，跳过下载：{TARGET_PATH}")
        return TARGET_PATH

    log(f"下载 WQY MicroHei（~4.6 MB）...")
    log(f"  来源：{FONT_URL}")

    def _progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            pct = min(100, downloaded * 100 // total_size)
            bar = "#" * (pct // 5) + "-" * (20 - pct // 5)
            print(f"\r  [{bar}] {pct}% ({downloaded//1024} KB)", end="", flush=True)

    try:
        urllib.request.urlretrieve(FONT_URL, TARGET_PATH, _progress)
        print()  # 换行
        log(f"下载完成：{TARGET_PATH}")
        return TARGET_PATH
    except Exception as e:
        print()
        log(f"下载失败：{e}")
        if os.path.exists(TARGET_PATH):
            os.remove(TARGET_PATH)
        sys.exit(1)


def main():
    ensure_dir()

    # 1. 已有
    found = already_have()
    if found:
        log(f"assets/fonts/ 已有字体：{found}，无需操作")
        return

    # 2. 系统字体
    sys_font = find_system_font()
    if sys_font:
        log(f"发现系统字体：{sys_font}")
        copy_system_font(sys_font)
        return

    # 3. 下载
    log("系统无 CJK 字体，开始下载...")
    download_font()

    log("完成！config.yaml 无需修改，运行时自动识别字体。")


if __name__ == "__main__":
    main()
