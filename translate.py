"""
translate.py — 将英文 .md 文件翻译成中文，生成 -zh.md 文件
使用 deep-translator（已安装，免费，无需 API Key）

用法：
  python translate.py <源文件.md>                  # 输出到同目录 *-zh.md
  python translate.py <源文件.md> <输出文件.md>     # 指定输出路径
  python translate.py --batch <目录>               # 批量翻译（跳过已有 -zh.md 的）
"""

import sys
import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator

CHUNK_SIZE = 4000  # Google Translate 单次上限约 5000，保守取 4000


def _safe_translate(translator: GoogleTranslator, text: str) -> str:
    """带重试的单行/段落翻译。"""
    if not text.strip():
        return text
    for attempt in range(3):
        try:
            result = translator.translate(text)
            return result if result else text
        except Exception as e:
            if attempt == 2:
                print(f"  [警告] 翻译失败，保留原文: {text[:60]}... ({e})")
                return text
            time.sleep(1.5)
    return text


def translate_markdown(content: str) -> str:
    """翻译 Markdown 内容，保留代码块、标题前缀、列表前缀。"""
    translator = GoogleTranslator(source="en", target="zh-CN")
    lines = content.split("\n")
    result = []
    in_code_block = False
    buffer_lines = []   # 普通段落缓冲
    buffer_len = 0

    def flush_buffer():
        nonlocal buffer_lines, buffer_len
        if not buffer_lines:
            return
        chunk = "\n".join(buffer_lines)
        result.append(_safe_translate(translator, chunk))
        buffer_lines = []
        buffer_len = 0

    def add_to_buffer(line: str):
        nonlocal buffer_len
        # 若加入会超限则先刷新
        if buffer_len + len(line) > CHUNK_SIZE:
            flush_buffer()
        buffer_lines.append(line)
        buffer_len += len(line)

    for line in lines:
        # 代码块开关
        if line.strip().startswith("```"):
            flush_buffer()
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # 空行：刷新缓冲，直接保留
        if not line.strip():
            flush_buffer()
            result.append(line)
            continue

        # Markdown 标题（# ## 等）：只翻译文字部分
        m = re.match(r"^(#{1,6}\s+)(.*)", line)
        if m:
            flush_buffer()
            prefix, text = m.groups()
            result.append(prefix + _safe_translate(translator, text))
            continue

        # 列表项（- * + 或 1. 2. 等）
        m = re.match(r"^(\s*[-*+]\s+|\s*\d+\.\s+)(.*)", line)
        if m:
            flush_buffer()
            prefix, text = m.groups()
            result.append(prefix + _safe_translate(translator, text))
            continue

        # 普通段落行：加入缓冲
        add_to_buffer(line)

    flush_buffer()
    return "\n".join(result)


def translate_file(src: Path, dst: Path):
    print(f"翻译: {src.name}")
    content = src.read_text(encoding="utf-8")
    translated = translate_markdown(content)
    header = f"<!-- 自动翻译自 {src.name}，由 translate.py 生成 -->\n\n"
    dst.write_text(header + translated, encoding="utf-8")
    print(f"  完成 → {dst.name}")


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    if args[0] == "--batch":
        if len(args) < 2:
            print("用法: python translate.py --batch <目录>")
            return
        base = Path(args[1])
        files = [
            f for f in base.rglob("*.md")
            if not f.stem.endswith("-zh") and not f.stem.endswith("_zh")
        ]
        print(f"找到 {len(files)} 个英文 .md 文件")
        for f in files:
            dst = f.with_name(f.stem + "-zh" + f.suffix)
            if dst.exists():
                print(f"  跳过（已存在）: {dst.name}")
                continue
            try:
                translate_file(f, dst)
            except Exception as e:
                print(f"  [错误] {f.name}: {e}")
        print("批量翻译完成。")

    else:
        src = Path(args[0])
        if not src.exists():
            print(f"文件不存在: {src}")
            return
        dst = Path(args[1]) if len(args) >= 2 else src.with_name(src.stem + "-zh" + src.suffix)
        translate_file(src, dst)


if __name__ == "__main__":
    main()
