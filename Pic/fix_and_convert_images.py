import os
from pathlib import Path
from PIL import Image

# =============== 配置区域 ===============
# 扫描的图片目录
IMAGE_DIR = Path("D:/Coding/java/bot_test/bot_test/src/main/resources/Pic/maomao")   # ← 改成你的实际目录
# 是否删除原文件
DELETE_ORIGINAL = True
# ======================================


def is_webp(file_path: Path) -> bool:
    """判断文件是否是 WebP 格式（检查文件头 RIFF....WEBP）"""
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


def convert_to_jpg(file_path: Path):
    """把任意图片转换为 JPG 格式"""
    try:
        with Image.open(file_path) as img:
            # 有些 PNG 带透明通道，要去掉 alpha
            if img.mode in ("RGBA", "LA"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1])  # 用 alpha 通道作 mask
                img = bg
            else:
                img = img.convert("RGB")

            out_path = file_path.with_suffix(".jpg")
            img.save(out_path, "JPEG", quality=90)
            print(f"✅ 转换完成: {file_path.name} → {out_path.name}")

            if DELETE_ORIGINAL and file_path != out_path:
                try:
                    file_path.unlink()
                    print(f"🗑️ 已删除原文件: {file_path.name}")
                except Exception as e:
                    print(f"⚠️ 删除失败 {file_path}: {e}")

    except Exception as e:
        print(f"❌ 转换失败: {file_path} ({e})")


def scan_and_fix(directory: Path):
    """扫描目录，检测并转换图片"""
    count_total = 0
    count_converted = 0

    for root, _, files in os.walk(directory):
        for name in files:
            file_path = Path(root) / name
            lower = name.lower()

            if not lower.endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue

            count_total += 1

            # WebP 或 PNG 都转为 JPG
            if is_webp(file_path) or lower.endswith(".png"):
                convert_to_jpg(file_path)
                count_converted += 1

    print(f"\n✅ 扫描完成：共检查 {count_total} 个文件，其中转换 {count_converted} 个为 JPG。")


if __name__ == "__main__":
    if not IMAGE_DIR.exists():
        print(f"目录不存在: {IMAGE_DIR}")
    else:
        scan_and_fix(IMAGE_DIR)
