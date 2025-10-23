#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
按序重命名指定目录下的所有图片文件为 1,2,3...
用法示例:
    python rename_images.py /path/to/dir --prefix "" --start 1 --sort name
参数:
    path    要处理的目录（必需）
    --prefix 新文件名前缀（默认空，结果如 1.jpg 或 img1.jpg）
    --start  起始编号（默认 1）
    --sort   排序方式: name 或 mtime（默认 name）
"""

import argparse
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif", ".heic"}

def natural_key(s: str):
    parts = re.split(r'(\d+)', s)
    return [int(p) if p.isdigit() else p.lower() for p in parts]

def find_images(folder: Path):
    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    return files

def safe_rename(src: Path, dst: Path):
    if src.resolve() == dst.resolve():
        return
    if dst.exists():
        tmp = dst.with_suffix(dst.suffix + ".tmp_renaming")
        src.rename(tmp)
        tmp.replace(dst)
    else:
        src.replace(dst)

def main():
    p = argparse.ArgumentParser(description="批量按序重命名图片")
    p.add_argument("path", help="目标目录路径")
    p.add_argument("--prefix", default="", help="重命名前缀，默认无（直接数字）")
    p.add_argument("--start", type=int, default=1, help="起始编号，默认 1")
    p.add_argument("--sort", choices=("name", "mtime"), default="name", help="排序方式: name 或 mtime")
    p.add_argument("--pad", type=int, default=0, help="编号左侧填充宽度（0 表示不填充）")
    args = p.parse_args()

    folder = Path(args.path)
    if not folder.exists() or not folder.is_dir():
        print("错误: 指定路径不存在或不是目录。")
        return

    imgs = find_images(folder)
    if not imgs:
        print("目录中未找到支持的图片文件。")
        return

    if args.sort == "name":
        imgs.sort(key=lambda p: natural_key(p.name))
    else:
        imgs.sort(key=lambda p: p.stat().st_mtime)

    # 先生成目标名，检测冲突
    mappings = []
    n = args.start
    for src in imgs:
        ext = src.suffix.lower()
        num = str(n).zfill(args.pad) if args.pad > 0 else str(n)
        new_name = f"{args.prefix}{num}{ext}"
        dst = folder / new_name
        mappings.append((src, dst))
        n += 1

    # 如果目标名与源名完全一致则跳过
    # 如果存在目标名与其他源冲突（例如要改成现有文件名），先做两步临时改名
    collisions = any(dst.exists() and dst not in [s for s, _ in mappings] for _, dst in mappings)
    if collisions:
        # 临时重命名所有要改的文件到不可见中间名
        temp_map = []
        for i, (src, dst) in enumerate(mappings):
            tmp = folder / f".rename_tmp_{datetime.now().timestamp()}_{i}{src.suffix}"
            src.rename(tmp)
            temp_map.append((tmp, dst))
        # 再把临时名改回目标名
        for tmp, dst in temp_map:
            safe_rename(tmp, dst)
    else:
        for src, dst in mappings:
            safe_rename(src, dst)

    print(f"已完成重命名，共处理 {len(mappings)} 个文件。")

if __name__ == "__main__":
    main()
