#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
素材完整性检查工具
用于检查项目的 script.json 中的素材路径是否与实际文件匹配

使用方法:
    python check_assets.py <project_name>
    python check_assets.py day4
    python check_assets.py day6 day7  # 批量检查
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple


def get_project_root() -> Path:
    """获取项目根目录"""
    # 获取脚本所在目录的父目录
    script_dir = Path(__file__).resolve().parent
    # 如果脚本在项目根目录，直接使用
    if (script_dir / "script.json").exists():
        return script_dir
    # 否则返回脚本目录
    return script_dir


def scan_assets_dir(assets_dir) -> Dict[str, List[str]]:
    """
    扫描 assets 目录，建立文件名索引
    返回: {文件名(无后缀): [完整文件名列表]}
    """
    index = {}
    
    for subdir in ['images', 'manual', 'manim', 'videos', 'avatar']:
        dir_path = assets_dir / subdir
        if not dir_path.exists():
            continue
        
        for f in dir_path.iterdir():
            if f.is_file():
                # 建立索引：去掉后缀作为 key
                name_without_ext = f.stem
                if name_without_ext not in index:
                    index[name_without_ext] = []
                index[name_without_ext].append(f.name)
    
    return index


def check_project(project_name: str, project_root: Path) -> Tuple[int, int, List[Dict]]:
    """
    检查单个项目的素材完整性
    
    返回: (错误数, 警告数, 问题列表)
    """
    project_dir = project_root / "projects" / project_name
    script_path = project_dir / "script.json"
    assets_dir = project_dir / "assets"
    
    errors = []
    warnings = []
    
    # 1. 检查 script.json 是否存在
    if not script_path.exists():
        print(f"❌ 项目 '{project_name}' 不存在或没有 script.json")
        return 1, 0, [{"type": "error", "msg": "script.json not found"}]
    
    # 2. 扫描素材目录
    assets_index = scan_assets_dir(assets_dir)
    
    # 3. 解析 script.json
    with open(script_path, 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    print(f"\n{'='*60}")
    print(f"📁 项目: {project_name}")
    print(f"   场景数: {len(scenes)}")
    print(f"   素材索引: {len(assets_index)} 个文件")
    print(f"{'='*60}")
    
    # 4. 检查每个场景的素材
    for scene in scenes:
        scene_id = scene.get('id', 'unknown')
        visual = scene.get('visual', {})
        vtype = visual.get('type', '')
        source = visual.get('source', '')
        
        if not source:
            continue
        
        # 检查文件是否存在
        file_exists = False
        found_path = None
        
        # 尝试多种路径
        paths_to_try = [
            source,  # 原始路径
            str(project_dir / source),  # 绝对路径
            str(assets_dir / "manual" / source.split('/')[-1]),  # manual 目录
            str(assets_dir / "images" / source.split('/')[-1]),  # images 目录
        ]
        
        for path in paths_to_try:
            if os.path.exists(path):
                file_exists = True
                found_path = path
                break
        
        # 如果直接路径不存在，尝试智能匹配
        if not file_exists:
            # 提取文件名（去掉扩展名）
            base_name = os.path.splitext(os.path.basename(source))[0]
            
            # 在索引中查找匹配
            for idx_name, files in assets_index.items():
                # 检查是否包含 base_name
                if base_name in idx_name or idx_name in base_name:
                    file_exists = True
                    found_path = str(assets_dir / "manual" / files[0])
                    warnings.append({
                        "scene": scene_id,
                        "type": "path_hint",
                        "msg": f"路径 '{source}' 不存在，但找到 '{files[0]}'",
                        "suggestion": f"将 script.json 中的 source 改为: assets/manual/{files[0]}"
                    })
                    break
        
        if not file_exists:
            errors.append({
                "scene": scene_id,
                "type": vtype,
                "source": source,
                "msg": f"素材不存在: {source}"
            })
    
    # 5. 输出结果
    if errors:
        print(f"\n❌ 发现 {len(errors)} 个错误:")
        for e in errors:
            print(f"   [{e['scene']}] ({e['type']}) {e['source']}")
    
    if warnings:
        print(f"\n⚠️  发现 {len(warnings)} 个警告:")
        for w in warnings:
            print(f"   [{w['scene']}] {w['msg']}")
            print(f"      💡 建议: {w['suggestion']}")
    
    if not errors and not warnings:
        print(f"\n✅ 所有素材路径正确!")
    
    return len(errors), len(warnings), errors + warnings


def main():
    project_root = get_project_root()
    
    if len(sys.argv) < 2:
        # 如果没有参数，列出所有项目
        projects_dir = project_root / "projects"
        if projects_dir.exists():
            projects = [d.name for d in projects_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
            print("可用项目:")
            for p in sorted(projects):
                print(f"   - {p}")
            print("\n使用方法: python check_assets.py <project_name>")
            print("示例: python check_assets.py day4")
        return
    
    # 批量检查
    project_names = sys.argv[1:]
    total_errors = 0
    total_warnings = 0
    
    for name in project_names:
        errors, warnings, _ = check_project(name, project_root)
        total_errors += errors
        total_warnings += warnings
    
    # 总结
    print(f"\n{'='*60}")
    print(f"📊 总计: {len(project_names)} 个项目")
    print(f"   错误: {total_errors}")
    print(f"   警告: {total_warnings}")
    
    if total_errors == 0 and total_warnings == 0:
        print("   ✅ 全部通过!")
    elif total_errors == 0:
        print("   ⚠️  有警告但不影响生成")
    else:
        print("   ❌ 有错误，需要修复后再生成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
