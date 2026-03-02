"""
auto_fetch_assets.py - 自动批量获取 needs_list 中的素材

策略：
  - clipart / image → 从 Pixabay 免费图库按关键词搜图下载（免费）
  - ai_image        → 调用 config.yaml 里的 image_gen API 生成（付费）
  - 任意步骤失败    → 自动生成灰色占位图兜底

Pixabay Key 读取顺序：
  1. config.yaml 的 pixabay.api_key（推荐）
  2. --pixabay-key 命令行参数（可覆盖 config）

用法：
  # 直接用（Key 已在 config.yaml 里配置好）
  python scripts/auto_fetch_assets.py --project projects/number2

  # 只预览，不实际下载
  python scripts/auto_fetch_assets.py --project projects/number2 --dry-run

  # 跳过已存在的文件（断点续传）
  python scripts/auto_fetch_assets.py --project projects/number2 --skip-existing
"""

import argparse
import json
import os
import re
import sys
import time
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config import load_config


# ── 工具函数 ────────────────────────────────────────────────────────────────

def _extract_keywords(description: str) -> str:
    """从 description 里提取 Keywords: 后面的英文关键词。"""
    m = re.search(r"[Kk]eywords?\s*[:：]\s*(.+)", description or "")
    if m:
        return m.group(1).strip().rstrip(".")
    # fallback：去掉中文，取首段英文
    english = re.sub(r"[\u4e00-\u9fff]+", "", description or "").strip()
    english = re.sub(r"\s+", " ", english).strip(" .。，")
    return english[:80] if english else "illustration"


def _make_ai_prompt(item: dict) -> str:
    """为 ai_image 类型构造 AI 生图 prompt。"""
    desc = item.get("description", "")
    if "[Prompt]" in desc:
        return desc.split("[Prompt]", 1)[1].strip()
    keywords = _extract_keywords(desc)
    return (
        f"{keywords}, digital art, cinematic lighting, 4k, detailed, abstract tech style"
    )


# ── Pixabay 免费下载 ─────────────────────────────────────────────────────────

PIXABAY_API = "https://pixabay.com/api/"

def download_from_pixabay(keywords: str, save_path: str, api_key: str) -> bool:
    """从 Pixabay 搜索并下载第一张匹配图片。"""
    try:
        params = {
            "key": api_key,
            "q": keywords,
            "image_type": "vector,illustration,clipart",
            "safesearch": "true",
            "per_page": 5,
            "min_width": 400,
        }
        r = requests.get(PIXABAY_API, params=params, timeout=15)
        r.raise_for_status()
        hits = r.json().get("hits", [])
        if not hits:
            # 再试一次用更简短的关键词
            short_kw = " ".join(keywords.split(",")[:2]).strip()
            params["q"] = short_kw
            params["image_type"] = "photo"
            r2 = requests.get(PIXABAY_API, params=params, timeout=15)
            r2.raise_for_status()
            hits = r2.json().get("hits", [])
        if not hits:
            return False
        # 优先选 webformatURL（中等分辨率，足够用）
        img_url = hits[0].get("webformatURL") or hits[0].get("previewURL")
        if not img_url:
            return False
        img_data = requests.get(img_url, timeout=20).content
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(img_data)
        return True
    except Exception as e:
        print(f"    [!] Pixabay 下载失败: {e}")
        return False


# ── AI 生图（付费，仅用于 ai_image 类型）────────────────────────────────────

def generate_image_ai(prompt: str, save_path: str, cfg) -> bool:
    """调用 image_gen API 生成图片。"""
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=cfg.image_gen.api_key,
            base_url=cfg.image_gen.base_url,
        )
        resp = client.images.generate(
            model=cfg.image_gen.model,
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        img_url = resp.data[0].url
        img_data = requests.get(img_url, timeout=30).content
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(img_data)
        return True
    except Exception as e:
        print(f"    [!] AI 生图失败: {e}")
        return False


# ── 占位图兜底 ──────────────────────────────────────────────────────────────

def create_placeholder(save_path: str, label: str) -> bool:
    """兜底：生成灰色占位图。"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (800, 800), color=(210, 210, 210))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf", 36)
        except Exception:
            font = ImageFont.load_default()
        draw.multiline_text(
            (80, 360), f"[Placeholder]\n{label[:40]}", fill=(90, 90, 90), font=font
        )
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        img.save(save_path)
        return True
    except Exception as e:
        print(f"    [!] 占位图失败（需要 Pillow）: {e}")
        return False


# ── 主逻辑 ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="自动批量获取 needs_list 素材")
    parser.add_argument("--project", required=True, help="项目目录")
    parser.add_argument("--pixabay-key", default="", help="Pixabay API Key（留空则读 config.yaml）")
    parser.add_argument("--config", default=None)
    parser.add_argument("--dry-run", action="store_true", help="只预览不下载")
    parser.add_argument("--skip-existing", action="store_true", help="跳过已存在文件")
    parser.add_argument("--delay", type=float, default=1.0, help="每次请求间隔（秒）")
    parser.add_argument(
        "--type",
        choices=["all", "clipart", "image", "ai_image"],
        default="all",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)

    # Pixabay Key：CLI 参数优先，否则从 config.yaml 读取
    pixabay_key = args.pixabay_key or cfg.pixabay.api_key

    # 读 needs JSON
    needs_path = os.path.join(BASE_DIR, args.project, "script_needs.json")
    if not os.path.exists(needs_path):
        print(f"[错误] 找不到 {needs_path}，请先运行 plan 阶段。")
        sys.exit(1)

    with open(needs_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    needs_list: list[dict] = data.get("needs_list", [])

    # 去重
    seen, unique = set(), []
    for item in needs_list:
        fname = item.get("filename", "")
        if fname and fname not in seen:
            seen.add(fname)
            unique.append(item)

    if args.type != "all":
        unique = [x for x in unique if x.get("type") == args.type]

    ai_count = sum(1 for x in unique if x.get("type") == "ai_image")
    free_count = len(unique) - ai_count

    print(f"\n{'='*55}")
    print(f"  项目    : {args.project}")
    print(f"  总素材  : {len(unique)} 项")
    print(f"  免费下载: {free_count} 张（Pixabay）")
    print(f"  AI 生图 : {ai_count} 张（付费 API）")
    if not args.pixabay_key and free_count > 0:
        print(f"\n  ⚠️  未传 --pixabay-key，clipart/image 将用占位图替代")
        print(f"     免费注册: https://pixabay.com/api/docs/")
    print(f"{'='*55}\n")

    success = skip = fail = 0

    for i, item in enumerate(unique, 1):
        itype = item.get("type", "image")
        filename = item.get("filename", "")
        scene_id = item.get("scene_id", "?")
        description = item.get("description", "")

        save_path = os.path.join(BASE_DIR, args.project, filename)
        label = f"[{i:02d}/{len(unique)}] {scene_id} ({itype})"

        if args.skip_existing and os.path.exists(save_path):
            print(f"  {label} ✓ 已存在，跳过")
            skip += 1
            continue

        keywords = _extract_keywords(description)
        print(f"  {label}")
        print(f"    关键词: {keywords[:70]}")
        print(f"    路径  : {filename}")

        if args.dry_run:
            print("    [dry-run]\n")
            continue

        ok = False

        if itype == "ai_image":
            # 付费 AI 生图
            prompt = _make_ai_prompt(item)
            print(f"    → 调用 AI 生图 API...")
            ok = generate_image_ai(prompt, save_path, cfg)
        else:
            # clipart / image → Pixabay 免费
            if args.pixabay_key:
                print(f"    → Pixabay 搜图...")
                ok = download_from_pixabay(keywords, save_path, args.pixabay_key)
            else:
                print(f"    → 无 Pixabay Key，生成占位图")

        if ok:
            print(f"    ✓ 成功")
            success += 1
        else:
            # 兜底占位图
            ok2 = create_placeholder(save_path, scene_id)
            if ok2:
                print(f"    ✓ 占位图已保存")
                success += 1
            else:
                print(f"    ✗ 失败")
                fail += 1

        time.sleep(args.delay)
        print()

    print(f"\n{'='*55}")
    print(f"  完成！成功={success}  跳过={skip}  失败={fail}")
    print(f"{'='*55}")
    if not args.dry_run:
        print(f"\n下一步：")
        print(f"  python pipeline.py build --project {args.project}")


if __name__ == "__main__":
    main()
