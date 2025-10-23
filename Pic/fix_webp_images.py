import os
from pathlib import Path
from PIL import Image

# ===== 配置区域 =====
# 要扫描的目录
IMAGE_DIR = Path("D:/Coding/java/bot_test/bot_test/src/main/resources/Pic/maomao")  # 改成你自己的目录
# 是否删除原 WebP 文件
DELETE_ORIGINAL = False
# 转换输出格式（"png" 或 "jpeg"）
OUTPUT_FORMAT = "png"
# ====================


def is_webp(file_path: Path) -> bool:
    """判断文件是否是 WebP（通过前 12 字节检查 RIFF...WEBP）"""
    try:
        with open(file_path, "rb") as f:
            header = f.read(12)
            return (
                len(header) >= 12
                and header[0:4] == b"RIFF"
                and header[8:12] == b"WEBP"
            )
    except Exception:
        return False


def convert_to_png(file_path: Path):
    """把 WebP 转成 PNG 或 JPEG"""
    try:
        with Image.open(file_path) as img:
            out_path = file_path.with_suffix(f".{OUTPUT_FORMAT}")
            img.save(out_path, OUTPUT_FORMAT.upper())
            print(f"✅ 转换完成: {file_path.name} → {out_path.name}")
            if DELETE_ORIGINAL:
                file_path.unlink()
    except Exception as e:
        print(f"❌ 转换失败: {file_path} ({e})")


def scan_and_fix(directory: Path):
    """扫描目录下的图片文件并自动转换"""
    count_webp = 0
    count_total = 0

    for root, _, files in os.walk(directory):
        for name in files:
            file_path = Path(root) / name
            lower_name = name.lower()

            if not lower_name.endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue

            count_total += 1
            if is_webp(file_path):
                count_webp += 1
                print(f"检测到 WebP 文件: {file_path}")
                convert_to_png(file_path)

    print(f"\n扫描完成，共检查 {count_total} 个文件，其中 {count_webp} 个为 WebP。")


if __name__ == "__main__":
    if not IMAGE_DIR.exists():
        print(f"目录不存在: {IMAGE_DIR}")
    else:
        scan_and_fix(IMAGE_DIR)
