"""AI 图片生成 - 支持 DashScope 原生 API 和 OpenAI 兼容 API"""

import json
import os
from typing import List

import httpx

from parser.script_parser import SceneItem

# 调用计数器文件
COUNTER_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".api_call_count.json")

# DashScope API endpoints
DASHSCOPE_BASE = "https://dashscope.aliyuncs.com/api/v1"
# 旧模型 (wanx-v1) 用这个
DASHSCOPE_T2I_URL = f"{DASHSCOPE_BASE}/services/aigc/text2image/image-synthesis"
# 新模型 (wan2.6-t2i / wan2.6-image) 用这个
DASHSCOPE_MULTIMODAL_URL = f"{DASHSCOPE_BASE}/services/aigc/multimodal-generation/generation"

# wan2.6 系列模型使用 multimodal 接口
WAN26_MODELS = {"wan2.6-t2i", "wan2.6-image", "wan2.6-i2v"}


def _load_counter() -> dict:
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            return json.load(f)
    return {"image_gen_calls": 0}


def _save_counter(data: dict):
    with open(COUNTER_FILE, "w") as f:
        json.dump(data, f)


def _dashscope_wan26_generate(api_key: str, model: str, prompt: str, size: str = "1024*1024") -> str:
    """
    DashScope wan2.6 系列文生图（multimodal-generation 接口，同步模式）。
    返回图片 URL。
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # wan2.6 使用 messages 格式
    payload = {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ]
        },
        "parameters": {
            "size": size,
            "enable_interleave": True,
        },
    }

    # 同步调用，生图可能需要较长时间
    resp = httpx.post(DASHSCOPE_MULTIMODAL_URL, headers=headers, json=payload, timeout=180)
    if resp.status_code != 200:
        raise RuntimeError(f"API 错误 {resp.status_code}: {resp.text}")
    data = resp.json()

    # 同步模式直接从 output 中提取图片
    output = data.get("output", {})

    # 格式1: output.choices[].message.content[] → image_url 或 image
    choices = output.get("choices", [])
    for choice in choices:
        msg = choice.get("message", {})
        content = msg.get("content", [])
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict):
                    url = c.get("image_url") or c.get("image")
                    if url:
                        return url

    # 格式2: output.results[].url 或 .content[]
    results = output.get("results", [])
    for r in results:
        if r.get("url"):
            return r["url"]
        if isinstance(r.get("content"), list):
            for c in r["content"]:
                url = c.get("image_url") or c.get("image")
                if url:
                    return url

    raise RuntimeError(f"无法提取图片 URL: {json.dumps(data, ensure_ascii=False)[:500]}")


def _dashscope_wanx_generate_async(api_key: str, model: str, prompt: str, size: str = "1024*1024") -> str:
    """
    DashScope 旧模型 (wanx-v1) 文生图（异步任务模式）。
    提交任务 -> 轮询 -> 返回图片 URL。
    """
    import time
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable", # 显式开启异步
    }

    payload = {
        "model": model,
        "input": {
            "prompt": prompt,
        },
        "parameters": {
            "size": size,
            "n": 1,
        },
    }

    # 1. 提交任务
    resp = httpx.post(DASHSCOPE_T2I_URL, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"API 提交错误 {resp.status_code}: {resp.text}")
    
    task_data = resp.json()
    task_id = task_data.get("output", {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"未获取到 task_id: {task_data}")

    print(f"      [task] 任务已提交: {task_id}，等待生成...")

    # 2. 轮询状态
    task_url = f"{DASHSCOPE_BASE}/tasks/{task_id}"
    start_time = time.time()
    
    while True:
        # 避免过于频繁轮询
        time.sleep(2)
        
        # 检查超时 (5分钟)
        if time.time() - start_time > 300:
            raise RuntimeError("生图任务超时")

        check_resp = httpx.get(task_url, headers=headers, timeout=30)
        if check_resp.status_code != 200:
            print(f"      [warn] 查询状态失败: {check_resp.status_code}")
            continue
            
        check_data = check_resp.json()
        status = check_data.get("output", {}).get("task_status", "")
        
        if status == "SUCCEEDED":
            results = check_data.get("output", {}).get("results", [])
            for r in results:
                if r.get("url"):
                    return r["url"]
            raise RuntimeError(f"任务成功但无图片 URL: {check_data}")
            
        elif status in ("FAILED", "CANCELED"):
            code = check_data.get("output", {}).get("code", "Unknown")
            msg = check_data.get("output", {}).get("message", "Unknown")
            raise RuntimeError(f"任务失败 ({code}): {msg}")
            
        # PENDING / RUNNING -> 继续轮询



def _openai_generate(api_key: str, base_url: str, model: str, prompt: str) -> str:
    """OpenAI 兼容接口生图，返回图片 URL。"""
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.images.generate(
        model=model,
        prompt=prompt,
        n=1,
        size="1024x1024",
    )
    return response.data[0].url


def generate_images(
    scenes: List[SceneItem],
    output_dir: str,
    api_key: str,
    base_url: str,
    model: str = "wan2.6-t2i",
    max_calls: int = 0,
) -> dict:
    """
    为 ai_image 类型的 scene 生成图片。
    自动检测 provider：base_url 含 dashscope → 原生 API，否则 OpenAI 兼容。
    """
    os.makedirs(output_dir, exist_ok=True)
    result = {}

    ai_scenes = [s for s in scenes if s.visual_type == "ai_image"]
    if not ai_scenes:
        return result

    use_dashscope = "dashscope" in base_url

    # 检查额度
    counter = _load_counter()
    used = counter.get("image_gen_calls", 0)
    if max_calls > 0:
        remaining = max_calls - used
        print(f"  [额度] 已用 {used}/{max_calls}，剩余 {remaining} 次")
        if remaining <= 0:
            print(f"  [warn] 额度已用完，跳过所有 AI 生图")
            return result

    if len(ai_scenes) > 10:
        print(f"\n  [warn] 当前脚本包含 {len(ai_scenes)} 张高频 AI 生图需求！")
        print(f"  [warn] 如果使用的是免费版的阿里云模型接口，极其容易触发并发限制导致失败。")
        print(f"  [warn] 建议减少使用 `ai_image` 数量，或者开通企业级服务提升并发额度。")
        print(f"  [warn] 脚本将继续... 如果报错退出，可以直接重新运行 build 命令恢复接续生成。\n")

    for scene in ai_scenes:
        output_path = os.path.join(output_dir, f"{scene.id}.png")

        # 已存在则跳过
        if os.path.exists(output_path):
            print(f"  [{scene.id}] 图片已存在，跳过")
            result[scene.id] = output_path
            continue

        # 检查额度
        if max_calls > 0 and counter.get("image_gen_calls", 0) >= max_calls:
            print(f"  [{scene.id}] 额度已用完，跳过")
            if scene.visual_fallback:
                print(f"           → 将使用 fallback: {scene.visual_fallback}")
            continue

        prompt = scene.visual_source
        if not prompt:
            print(f"  [{scene.id}] 无 prompt，跳过")
            continue

        try:
            print(f"  [{scene.id}] 生成中...")

            if use_dashscope:
                if model.startswith("qwen-image"):
                    # 使用标准 HTTP 请求调用 dashscope qwen-image (和 wan2.6 使用相同 Multimodal 接口)
                    image_url = _dashscope_wan26_generate(api_key, model, prompt)
                elif model == "wanx-v1":
                    image_url = _dashscope_wanx_generate_async(api_key, model, prompt)
                elif model in WAN26_MODELS:
                    image_url = _dashscope_wan26_generate(api_key, model, prompt)
                else:
                    image_url = _dashscope_wanx_generate_async(api_key, model, prompt)
            else:
                image_url = _openai_generate(api_key, base_url, model, prompt)

            # 计数 +1
            counter["image_gen_calls"] = counter.get("image_gen_calls", 0) + 1
            _save_counter(counter)

            # 下载图片
            img_resp = httpx.get(image_url, timeout=120, follow_redirects=True)
            img_resp.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(img_resp.content)

            result[scene.id] = output_path
            remaining = max_calls - counter["image_gen_calls"] if max_calls > 0 else "∞"
            print(f"  [{scene.id}] 完成 → {output_path} (剩余 {remaining} 次)")

        except Exception as e:
            print(f"  [{scene.id}] 图片生成失败: {e}")
            if scene.visual_fallback:
                print(f"           → 将使用 fallback: {scene.visual_fallback}")

    return result


if __name__ == "__main__":
    counter = _load_counter()
    print(f"当前已用: {counter.get('image_gen_calls', 0)} 次")
