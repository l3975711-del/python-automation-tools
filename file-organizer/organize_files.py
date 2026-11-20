#!/usr/bin/env python3
"""
文件整理小工具 file-organizer

把一个文件夹里散落的文件，按类型自动分到子文件夹里。

用法：
    python organize_files.py <文件夹路径> [--dry-run]

例子：
    python organize_files.py ~/Downloads
    python organize_files.py ~/Downloads --dry-run   # 只预览，不真的移动

分类：
    图片 Images      .jpg .jpeg .png .gif .bmp .webp .heic .svg
    文档 Documents   .pdf .doc .docx .txt .md .xls .xlsx .ppt .pptx .csv
    视频 Videos      .mp4 .mov .mkv .avi .wmv .flv
    音频 Audio       .mp3 .wav .flac .aac .ogg .m4a
    压缩包 Archives  .zip .rar .7z .tar .gz
    代码 Code        .py .js .ts .html .css .java .c .cpp .go .rs .json
    其他 Others      以上都不匹配的

特点：
- 只移动文件夹根目录下的文件，不动子文件夹
- 目标文件夹里已有同名文件时，自动改名：报告.pdf -> 报告 (1).pdf
- 不需要安装任何第三方库，Python 3.8+ 就能跑
"""

import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "图片 Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".svg"},
    "文档 Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "视频 Videos": {".mp4", ".mov", ".mkv", ".avi", ".wmv", ".flv"},
    "音频 Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "压缩包 Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "代码 Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".go", ".rs", ".json"},
}


def category_of(path: Path) -> str:
    suffix = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if suffix in exts:
            return name
    return "其他 Others"


def unique_target(folder: Path, name: str) -> Path:
    """目标已存在同名文件时，加 (1)、(2)... 避免覆盖。"""
    target = folder / name
    if not target.exists():
        return target
    stem, suffix = Path(name).stem, Path(name).suffix
    i = 1
    while True:
        candidate = folder / f"{stem} ({i}){suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def organize(folder: Path, dry_run: bool = False) -> dict:
    moved = {}
    for item in sorted(folder.iterdir()):
        # 只处理文件；跳过文件夹和本脚本自己
        if not item.is_file():
            continue
        if item.name == Path(__file__).name:
            continue
        category = category_of(item)
        dest_dir = folder / category
        target = unique_target(dest_dir, item.name)
        if dry_run:
            print(f"[预览] {item.name} -> {category}/{target.name}")
        else:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(target))
            print(f"已移动 {item.name} -> {category}/{target.name}")
        moved[category] = moved.get(category, 0) + 1
    return moved


def main():
    parser = argparse.ArgumentParser(description="按类型整理文件夹里的文件")
    parser.add_argument("folder", help="要整理的文件夹路径")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不真的移动文件")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        print(f"找不到文件夹：{folder}")
        raise SystemExit(1)

    print(f"正在整理：{folder}" + ("（预览模式）" if args.dry_run else ""))
    result = organize(folder, dry_run=args.dry_run)
    if not result:
        print("没有需要整理的文件。")
        return
    print()
    for category, count in sorted(result.items()):
        print(f"{category}：{count} 个")
    print(f"共 {sum(result.values())} 个文件" + ("（预览，未移动）" if args.dry_run else "已整理完毕"))


if __name__ == "__main__":
    main()
