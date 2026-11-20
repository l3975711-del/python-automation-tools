# 文件整理小工具 file-organizer

把一个文件夹里散落的文件，按类型自动分到子文件夹里。适合整理下载文件夹、桌面。

## 用法

```bash
python organize_files.py ~/Downloads
python organize_files.py ~/Downloads --dry-run   # 只预览，不真的移动
```

## 分类

| 文件夹 | 类型 |
| --- | --- |
| 图片 Images | .jpg .png .gif 等 |
| 文档 Documents | .pdf .docx .txt .xlsx .pptx 等 |
| 视频 Videos | .mp4 .mov .mkv 等 |
| 音频 Audio | .mp3 .wav 等 |
| 压缩包 Archives | .zip .rar .7z 等 |
| 代码 Code | .py .js .html 等 |
| 其他 Others | 以上都不匹配的 |

## 特点

- 只移动文件夹根目录下的文件，不动子文件夹
- 同名文件自动改名，不会覆盖：`报告.pdf` → `报告 (1).pdf`
- 无第三方依赖，Python 3.8+ 就能跑
