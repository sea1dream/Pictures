#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description="将指定目录下所有文件后缀改为 .jpg")
parser.add_argument("path", nargs="?", default=".", help="目标目录")
parser.add_argument("--dry-run", action="store_true", help="仅打印不执行")
parser.add_argument("--recursive", action="store_true", default=True, help="递归子目录 (默认开启)")
args = parser.parse_args()

p = Path(args.path)
if not p.exists() or not p.is_dir():
    print(f"目标目录不存在: {p}", file=sys.stderr)
    sys.exit(1)

files = p.rglob("*") if args.recursive else p.iterdir()

for f in files:
    if not f.is_file():
        continue
    if f.suffix.lower() == ".jpg":
        print(f"跳过 已是png: {f}")
        continue
    new = f.with_suffix(".jpg")
    if new == f:
        print(f"跳过 相同路径: {f}")
        continue
    if args.dry_run:
        print(f"[DRY] rename {f} -> {new}")
    else:
        print(f"rename {f} -> {new}")
        try:
            f.rename(new)
        except Exception as e:
            print(f"错误 重命名 {f} -> {new}: {e}", file=sys.stderr)
