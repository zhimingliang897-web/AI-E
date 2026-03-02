#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
免费剪贴画素材自动下载器

功能：
- 解析JSON中的needs_list，筛选type为'clipart'的条目（免费素材）
- 自动忽略ai_image、ai_video等其他类型
- 从多个免费图库搜索并下载：unDraw、Storyset、Wikimedia Commons、OpenMoji
- 智能本地检查，避免重复下载
- 详细的日志和错误处理

使用方法：
  python clipart_downloader.py projects/day2/script_needs.json
  python clipart_downloader.py projects/day2/script_needs.json --dry-run
  cat script_needs.json | python clipart_downloader.py

依赖库：requests
"""

import os
import sys
import json
import logging
import requests
import argparse
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse, quote
from datetime import datetime

# ==================== 日志配置 ====================
def setup_logging(log_file: str = 'asset_download.log') -> logging.Logger:
    """配置日志系统"""
    log_path = Path(log_file)
    
    # 创建logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    # 文件处理器
    file_handler = logging.FileHandler(log_path, encoding='utf-8', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

# ==================== 常量定义 ====================
DEFAULT_ASSETS_DIR = Path("assets/manual")

SUPPORTED_LIBRARIES = {
    "undraw": {
        "name": "unDraw",
        "homepage": "https://undraw.co",
        "license": "MIT",
        "requires_attribution": False,
        "priority": 1
    },
    "storyset": {
        "name": "Storyset",
        "homepage": "https://storyset.com",
        "license": "Free to use",
        "requires_attribution": False,
        "priority": 2
    },
    "wikimedia": {
        "name": "Wikimedia Commons",
        "homepage": "https://commons.wikimedia.org",
        "license": "Various (CC-BY, CC0, etc.)",
        "requires_attribution": True,
        "priority": 3
    },
    "openmoji": {
        "name": "OpenMoji",
        "homepage": "https://openmoji.org",
        "license": "CC BY-SA 4.0",
        "requires_attribution": True,
        "priority": 4
    }
}

TIMEOUT = 15
MAX_RETRIES = 2
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8"


# ==================== 文件操作 ====================
def ensure_assets_directory(assets_dir: Path) -> bool:
    """确保素材存储目录存在"""
    try:
        assets_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"✓ 目录已准备: {assets_dir.absolute()}")
        return True
    except Exception as e:
        logger.error(f"✗ 无法创建目录 {assets_dir}: {str(e)}")
        return False


def check_existing_file(scene_id: str, file_type: str, assets_dir: Path) -> bool:
    filename = f"{scene_id}_{file_type}.png"
    file_path = assets_dir / filename
    return check_existing_path(file_path)


def check_existing_path(file_path: Path) -> bool:
    if file_path.exists():
        file_size = file_path.stat().st_size
        if file_size > 1000:
            if _is_valid_image_path(file_path):
                logger.info(f"✓ 文件已存在（跳过）: {file_path.name} ({file_size} bytes)")
                return True
            logger.warning(f"⚠ 文件格式异常（重新下载）: {file_path.name}")
            file_path.unlink()
        else:
            logger.warning(f"⚠ 文件损坏（重新下载）: {file_path.name}")
            file_path.unlink()
    return False


def _is_valid_image_path(path: Path) -> bool:
    try:
        head = path.read_bytes()[:256]
    except Exception:
        return False
    ext = path.suffix.lower()
    if ext == ".png":
        return head.startswith(PNG_MAGIC)
    if ext in (".jpg", ".jpeg"):
        return head.startswith(JPEG_MAGIC)
    if ext == ".svg":
        stripped = head.lstrip(b"\xef\xbb\xbf").lstrip()
        return stripped.startswith(b"<?xml") or stripped.startswith(b"<svg")
    return True


def save_downloaded_file(response: requests.Response, save_path: Path) -> bool:
    """保存下载的文件"""
    try:
        # 验证响应内容
        content_type = response.headers.get('Content-Type', '').lower()
        if 'image' not in content_type and not save_path.suffix in ['.png', '.jpg', '.svg']:
            logger.debug(f"⚠ 无效的Content-Type: {content_type}")
            return False
        
        # 检查内容有效性（避免错误页面）
        if response.content[:4] == b'<html':
            logger.debug("⚠ 返回内容为HTML，不是有效图片")
            return False
        ext = save_path.suffix.lower()
        head = response.content[:256]
        if ext == ".png":
            if "webp" in content_type or "svg" in content_type or "xml" in content_type:
                logger.debug("⚠ 返回内容格式与PNG不匹配")
                return False
            if not head.startswith(PNG_MAGIC):
                logger.debug("⚠ PNG 头校验失败")
                return False
        elif ext in (".jpg", ".jpeg"):
            if "webp" in content_type or "svg" in content_type or "xml" in content_type:
                logger.debug("⚠ 返回内容格式与JPG不匹配")
                return False
            if not head.startswith(JPEG_MAGIC):
                logger.debug("⚠ JPG 头校验失败")
                return False
        elif ext == ".svg":
            stripped = head.lstrip(b"\xef\xbb\xbf").lstrip()
            if not (stripped.startswith(b"<?xml") or stripped.startswith(b"<svg")):
                logger.debug("⚠ SVG 头校验失败")
                return False
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        file_size = save_path.stat().st_size
        logger.info(f"✓ 已保存: {save_path.name} ({file_size} bytes)")
        return True
        
    except Exception as e:
        logger.error(f"✗ 保存文件失败: {str(e)}")
        if save_path.exists():
            save_path.unlink()
        return False


# ==================== JSON输入处理 ====================
def extract_clipart_needs(data: Dict) -> List[Dict]:
    """
    从输入数据中提取所有type为'clipart'的需求项
    
    Args:
        data: JSON解析后的输入数据
    
    Returns:
        clipart类型需求列表
    """
    needs_list = data.get("needs_list", [])
    clipart_items = []
    
    for item in needs_list:
        if item.get("type") == "clipart":
            scene_id = item.get("scene_id")
            description = item.get("description", "")
            
            if not scene_id:
                logger.warning("⚠ 发现缺少scene_id的clipart条目，已跳过")
                continue
            
            clipart_items.append({
                "scene_id": scene_id,
                "description": description,
                "is_optional": item.get("is_optional", False),
                "filename": item.get("filename")
            })
    
    if clipart_items:
        logger.info(f"📋 共筛选出 {len(clipart_items)} 个clipart下载任务")
    else:
        logger.warning("⚠ 未找到需要处理的clipart项目")
    
    return clipart_items


def load_input_json(input_source: Optional[str] = None) -> Optional[Dict]:
    """
    从文件或stdin读取JSON数据
    
    Args:
        input_source: JSON文件路径，如果为None则从stdin读取
    
    Returns:
        解析后的JSON对象，失败返回None
    """
    try:
        if input_source:
            json_path = Path(input_source)
            if not json_path.exists():
                logger.error(f"✗ 输入文件不存在: {json_path}")
                return None
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"✓ 已读取JSON文件: {json_path}")
        else:
            # 从stdin读取
            input_data = sys.stdin.read()
            if not input_data.strip():
                raise ValueError("输入为空")
            data = json.loads(input_data)
            logger.info("✓ 已从stdin读取JSON数据")
        
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"✗ JSON解析失败: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"✗ 读取输入失败: {str(e)}")
        return None


# ==================== 关键词生成 ====================
def build_search_keywords(scene_id: str, description: str) -> List[str]:
    """
    构建搜索关键词列表
    
    Args:
        scene_id: 场景ID
        description: 描述文本
    
    Returns:
        关键词列表（已去重）
    """
    keywords = []
    
    # 从scene_id提取关键词
    if '_' in scene_id:
        scene_parts = scene_id.split('_')
        # 跳过数字开头的部分，取后续的实质性词汇
        scene_words = [p for p in scene_parts[1:] if not p.isdigit()]
        keywords.extend(scene_words)
    
    # 从描述中提取关键词
    if description:
        # 提取中英文关键词（简化处理，对中文不分词）
        import re
        # 保留字母数字和中文
        words = re.findall(r'[\w]+', description)
        
        # 过滤英文停用词
        stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'are', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'use', 'using', 'also', 'or'
        }
        
        filtered_words = [
            w.lower() for w in words 
            if w.lower() not in stop_words and len(w) > 1
        ]
        keywords.extend(filtered_words[:5])  # 限制描述中的关键词数量
    
    # 去重并保持顺序
    seen = set()
    unique_keywords = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower not in seen and len(kw_lower) > 0:
            seen.add(kw_lower)
            unique_keywords.append(kw_lower)
    
    logger.debug(f"🔑 {scene_id} 的搜索关键词: {unique_keywords}")
    return unique_keywords[:8]  # 限制关键词总数


# ==================== 图库下载功能 ====================
class LibraryDownloader:
    """图库下载器基类"""
    
    def __init__(self, headers: Dict = None):
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
    
    def __del__(self):
        try:
            self.session.close()
        except:
            pass


class UnDrawDownloader(LibraryDownloader):
    """unDraw下载器"""
    
    def download(self, keywords: List[str], save_path: Path) -> bool:
        """尝试从unDraw下载"""
        # unDraw API: https://undraw.co/api/illustrations?search=keyword
        # 返回SVG，我们转换为PNG
        
        for keyword in keywords:
            try:
                # 使用unDraw的API搜索插画
                api_url = f"https://undraw.co/api/illustrations?search={quote(keyword)}"
                
                response = self.session.get(api_url, timeout=TIMEOUT)
                if response.status_code != 200:
                    continue
                
                data = response.json()
                illustrations = data.get('illustrations', [])
                
                if not illustrations:
                    logger.debug(f"  unDraw未找到: {keyword}")
                    continue
                
                # 获取第一个匹配结果的SVG下载链接
                illustration = illustrations[0]
                svg_url = illustration.get('url')  # unDraw提供的页面URL
                
                if not svg_url:
                    continue
                
                # unDraw的下载链接通常为：https://undraw.co/download/filename
                # 这里采用备选方案：直接访问SVG或使用webp格式
                download_url = f"{svg_url}svg"  # 或 f"{svg_url}webp"
                
                img_response = self.session.get(download_url, stream=True, timeout=TIMEOUT)
                if img_response.status_code == 200:
                    if save_downloaded_file(img_response, save_path):
                        logger.info(f"  ✓ unDraw: {keyword}")
                        return True
                
            except requests.RequestException as e:
                logger.debug(f"  ✗ unDraw请求失败 ({keyword}): {str(e)}")
            except Exception as e:
                logger.debug(f"  ✗ unDraw处理失败 ({keyword}): {str(e)}")
        
        return False


class StorysetDownloader(LibraryDownloader):
    """Storyset下载器"""
    
    def download(self, keywords: List[str], save_path: Path) -> bool:
        """尝试从Storyset下载"""
        # Storyset搜索URL: https://storyset.com/search?q=keyword
        # 实际下载通常需要解析页面获取PNG链接
        
        for keyword in keywords:
            try:
                # 搜索页面
                search_url = f"https://storyset.com/search?q={quote(keyword)}"
                
                response = self.session.get(search_url, timeout=TIMEOUT)
                if response.status_code != 200:
                    continue
                
                # 简单启发式：寻找.png的链接
                import re
                png_urls = re.findall(r'https://[^"\s<>]+\.png', response.text)
                
                if not png_urls:
                    logger.debug(f"  Storyset未找到: {keyword}")
                    continue
                
                # 使用第一个找到的PNG
                for png_url in png_urls[:3]:
                    img_response = self.session.get(png_url, stream=True, timeout=TIMEOUT)
                    if img_response.status_code == 200 and save_downloaded_file(img_response, save_path):
                        logger.info(f"  ✓ Storyset: {keyword}")
                        return True
                
            except requests.RequestException as e:
                logger.debug(f"  ✗ Storyset请求失败 ({keyword}): {str(e)}")
            except Exception as e:
                logger.debug(f"  ✗ Storyset处理失败 ({keyword}): {str(e)}")
        
        return False


class WikimediaDownloader(LibraryDownloader):
    """Wikimedia Commons下载器"""
    
    def download(self, keywords: List[str], save_path: Path) -> bool:
        """通过Wikimedia API搜索并下载"""
        
        api_url = "https://commons.wikimedia.org/w/api.php"
        
        for keyword in keywords:
            try:
                # MediaWiki API搜索
                params = {
                    'action': 'query',
                    'format': 'json',
                    'list': 'search',
                    'srsearch': keyword,
                    'srprop': 'size',
                    'srlimit': 5,
                    'srnamespace': 6,  # File命名空间
                    'utf8': 1
                }
                
                response = self.session.get(api_url, params=params, timeout=TIMEOUT)
                if response.status_code != 200:
                    continue
                
                data = response.json()
                search_results = data.get('query', {}).get('search', [])
                
                if not search_results:
                    logger.debug(f"  Wikimedia未找到: {keyword}")
                    continue
                
                # 获取第一个结果的文件信息
                result = search_results[0]
                file_title = result['title']  # 格式: File:Xxxxx.ext
                
                # 获取文件的直接链接
                file_info_params = {
                    'action': 'query',
                    'titles': file_title,
                    'prop': 'imageinfo',
                    'iiprop': 'url',
                    'format': 'json'
                }
                
                info_response = self.session.get(api_url, params=file_info_params, timeout=TIMEOUT)
                if info_response.status_code != 200:
                    continue
                
                info_data = info_response.json()
                pages = info_data.get('query', {}).get('pages', {})
                
                for page_id, page_info in pages.items():
                    img_info = page_info.get('imageinfo', [])
                    if img_info:
                        image_url = img_info[0]['url']
                        
                        img_response = self.session.get(image_url, stream=True, timeout=TIMEOUT)
                        if img_response.status_code == 200:
                            if save_downloaded_file(img_response, save_path):
                                logger.info(f"  ✓ Wikimedia: {keyword}")
                                return True
                
            except requests.RequestException as e:
                logger.debug(f"  ✗ Wikimedia请求失败 ({keyword}): {str(e)}")
            except Exception as e:
                logger.debug(f"  ✗ Wikimedia处理失败 ({keyword}): {str(e)}")
        
        return False


class OpenMojiDownloader(LibraryDownloader):
    """OpenMoji下载器"""
    
    def download(self, keywords: List[str], save_path: Path) -> bool:
        """尝试从OpenMoji下载"""
        # OpenMoji API: https://cdn.jsdelivr.net/npm/openmoji@latest/data/openmoji.json
        
        try:
            # 获取OpenMoji索引
            api_url = "https://cdn.jsdelivr.net/npm/openmoji@latest/data/openmoji.json"
            
            response = self.session.get(api_url, timeout=TIMEOUT)
            if response.status_code != 200:
                return False
            
            emojis = response.json()
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # 在emoji数据中搜索匹配的标签
                for emoji in emojis:
                    tags = emoji.get('tags', '').lower()
                    if keyword_lower in tags:
                        # 构建PNG下载链接
                        hexcode = emoji['hexcode'].lower()
                        png_url = f"https://cdn.jsdelivr.net/npm/openmoji@latest/color/svg/{hexcode}.svg"
                        
                        img_response = self.session.get(png_url, stream=True, timeout=TIMEOUT)
                        if img_response.status_code == 200:
                            if save_downloaded_file(img_response, save_path):
                                logger.info(f"  ✓ OpenMoji: {keyword}")
                                return True
                        break
            
        except Exception as e:
            logger.debug(f"  ✗ OpenMoji处理失败: {str(e)}")
        
        return False


# ==================== 主下载逻辑 ====================
def download_clipart_asset(
    scene_id: str,
    keywords: List[str],
    assets_dir: Path,
    filename: Optional[str] = None
) -> Dict[str, bool]:
    """
    下载单个场景的图片素材
    
    Args:
        scene_id: 场景ID
        keywords: 搜索关键词
        assets_dir: 资源目录
    
    Returns:
        下载结果字典
    """
    result = {
        'illustration': False,
        'icon': False
    }
    
    if filename:
        target_name = Path(filename).name
        target_path = assets_dir / target_name
        role = "icon" if "_icon" in target_path.stem else "illustration"

        if check_existing_path(target_path):
            result[role] = True
            return result

        downloaders = [
            ("unDraw", UnDrawDownloader(HEADERS)),
            ("Storyset", StorysetDownloader(HEADERS)),
            ("Wikimedia", WikimediaDownloader(HEADERS)),
            ("OpenMoji", OpenMojiDownloader(HEADERS))
        ]

        logger.info(f"📥 下载{role}: {target_name}")
        for name, downloader in downloaders:
            if downloader.download(keywords, target_path):
                result[role] = True
                break

        if not result[role]:
            logger.warning(f"⚠ 未能下载: {target_name}")
        return result

    illustration_path = assets_dir / f"{scene_id}_illustration.png"
    icon_path = assets_dir / f"{scene_id}_icon.png"
    
    # 检查是否已存在
    if check_existing_file(scene_id, "illustration", assets_dir):
        result['illustration'] = True
    else:
        # 初始化下载器
        downloaders = [
            ("unDraw", UnDrawDownloader(HEADERS)),
            ("Storyset", StorysetDownloader(HEADERS)),
            ("Wikimedia", WikimediaDownloader(HEADERS)),
            ("OpenMoji", OpenMojiDownloader(HEADERS))
        ]
        
        logger.info(f"📥 下载illustration: {scene_id}_illustration.png")
        for name, downloader in downloaders:
            if downloader.download(keywords, illustration_path):
                result['illustration'] = True
                break
        
        if not result['illustration']:
            logger.warning(f"⚠ 未能下载: {scene_id}_illustration.png")
    
    # 下载图标（使用相同策略或添加特定后缀）
    if check_existing_file(scene_id, "icon", assets_dir):
        result['icon'] = True
    else:
        icon_keywords = [kw + "_icon" for kw in keywords] + keywords
        
        logger.info(f"📥 下载icon: {scene_id}_icon.png")
        downloaders = [
            ("unDraw", UnDrawDownloader(HEADERS)),
            ("Storyset", StorysetDownloader(HEADERS)),
            ("Wikimedia", WikimediaDownloader(HEADERS)),
            ("OpenMoji", OpenMojiDownloader(HEADERS))
        ]
        
        for name, downloader in downloaders:
            if downloader.download(icon_keywords, icon_path):
                result['icon'] = True
                break
        
        if not result['icon']:
            logger.warning(f"⚠ 未能下载: {scene_id}_icon.png")
    
    return result


# ==================== 主程序 ====================
def main():
    """主函数入口"""
    
    # 命令行参数
    parser = argparse.ArgumentParser(
        description='工程剪贴画素材自动下载器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  python clipart_downloader_v2.py projects/day2/script_needs.json
  python clipart_downloader_v2.py script_needs.json --output assets/manual
  cat script_needs.json | python clipart_downloader_v2.py
        '''
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        default=None,
        help='输入JSON文件路径（不指定则从stdin读取）'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=DEFAULT_ASSETS_DIR,
        help=f'输出目录（默认: {DEFAULT_ASSETS_DIR}）'
    )
    parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='仅显示要下载的任务，不实际下载'
    )
    parser.add_argument(
        '-l', '--list-libraries',
        action='store_true',
        help='显示支持的图库列表'
    )
    
    args = parser.parse_args()
    
    # 显示支持的图库
    if args.list_libraries:
        print("\n📚 支持的图库:")
        for key, lib_info in SUPPORTED_LIBRARIES.items():
            print(f"  • {lib_info['name']}")
            print(f"    URL: {lib_info['homepage']}")
            print(f"    License: {lib_info['license']}")
            print()
        return
    
    logger.info("=" * 60)
    logger.info("🚀 工程剪贴画素材下载器 v2.0 启动")
    logger.info(f"📂 输出目录: {args.output.absolute()}")
    logger.info("=" * 60)
    
    try:
        # 1. 加载输入数据
        input_data = load_input_json(args.input)
        if input_data is None:
            sys.exit(1)
        
        # 2. 提取clipart需求
        clipart_tasks = extract_clipart_needs(input_data)
        if not clipart_tasks:
            logger.info("✓ 任务完成（无需要处理的clipart项）")
            return
        
        # 3. DRY RUN模式
        if args.dry_run:
            logger.info("\n📋 DRY-RUN 模式（仅列出任务）:")
            for i, task in enumerate(clipart_tasks, 1):
                optional = "（可选）" if task['is_optional'] else ""
                logger.info(f"  {i}. {task['scene_id']} {optional}")
                logger.info(f"     描述: {task['description'][:60]}...")
            logger.info(f"\n共 {len(clipart_tasks)} 个任务准备就绪")
            return
        
        # 4. 确保目录存在
        if not ensure_assets_directory(args.output):
            sys.exit(1)
        
        # 5. 处理每个任务
        success_stats = {
            'illustration': 0,
            'icon': 0,
            'total_assets': 0
        }
        expected_assets = 0
        
        logger.info(f"\n📊 开始处理 {len(clipart_tasks)} 个任务...\n")
        
        for idx, task in enumerate(clipart_tasks, 1):
            scene_id = task["scene_id"]
            description = task["description"]
            is_optional = task.get("is_optional", False)
            
            optional_suffix = " [可选]" if is_optional else ""
            logger.info(f"\n[{idx}/{len(clipart_tasks)}] 处理: {scene_id}{optional_suffix}")
            
            # 构建关键词
            keywords = build_search_keywords(scene_id, description)
            
            filename = task.get("filename")
            role = None
            target_name = None
            if filename:
                target_name = Path(filename).name
                role = "icon" if "_icon" in Path(filename).stem else "illustration"
                expected_assets += 1
            else:
                expected_assets += 2

            result = download_clipart_asset(scene_id, keywords, args.output, filename)
            
            # 统计成功数量
            if role:
                if result[role]:
                    success_stats[role] += 1
                else:
                    logger.warning(f"  ⚠ {target_name} 下载失败")
            else:
                if result['illustration']:
                    success_stats['illustration'] += 1
                else:
                    logger.warning(f"  ⚠ {scene_id}_illustration.png 下载失败")
                
                if result['icon']:
                    success_stats['icon'] += 1
                else:
                    logger.warning(f"  ⚠ {scene_id}_icon.png 下载失败")
            
            success_stats['total_assets'] += sum(result.values())
        
        # 6. 输出汇总报告
        logger.info("\n" + "=" * 60)
        logger.info("✅ 任务完成总结")
        logger.info("=" * 60)
        logger.info(f"总计任务数: {len(clipart_tasks)}")
        logger.info(f"成功下载illustration: {success_stats['illustration']}/{len(clipart_tasks)}")
        logger.info(f"成功下载icon: {success_stats['icon']}/{len(clipart_tasks)}")
        logger.info(f"总共获取资产: {success_stats['total_assets']}/{expected_assets}")
        logger.info(f"资源保存位置: {args.output.absolute()}")
        logger.info(f"日志文件: {Path('asset_download.log').absolute()}")
        logger.info("=" * 60)
        
    except KeyboardInterrupt:
        logger.warning("\n⚠ 用户中断下载")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"❌ 程序执行过程中发生致命错误: {str(e)}")
        import traceback
        logger.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
