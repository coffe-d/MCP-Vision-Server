"""MCP Vision Server — Image recognition via Kimi/Moonshot API.

Provides two MCP tools:
- describe_image: Return image description as text
- describe_image_to_file: Save image description to a UTF-8 file

Environment variables:
- KIMI_API_KEY (required): Your Moonshot API key
- KIMI_BASE_URL (optional): API base URL, defaults to https://api.moonshot.cn/v1
- KIMI_MODEL (optional): Model name, defaults to moonshot-v1-8k-vision-preview
"""

import base64
import os
import sys
from pathlib import Path

from openai import OpenAI
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("vision-server")

KIMI_API_KEY = os.environ.get("KIMI_API_KEY", "")
KIMI_BASE_URL = os.environ.get("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
KIMI_MODEL = os.environ.get("KIMI_MODEL", "moonshot-v1-8k-vision-preview")

if not KIMI_API_KEY:
    print(
        "ERROR: KIMI_API_KEY environment variable is not set.\n"
        "Please set it before running the server:\n"
        '  export KIMI_API_KEY="sk-..."\n'
        "Get your key from https://platform.moonshot.cn/console/api-keys",
        file=sys.stderr,
    )
    sys.exit(1)

client = OpenAI(api_key=KIMI_API_KEY, base_url=KIMI_BASE_URL)

MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
}

MAX_IMAGE_BYTES = 20 * 1024 * 1024  # 20MB

DEFAULT_SYSTEM_PROMPT = (
    "你是一个图片内容识别助手。请详细描述图片中的内容，包括物体、文字、场景、"
    "人物等所有可见元素。如果图片中有文字，请准确地提取出来。"
)


def _encode_image(image_path: str) -> tuple[str, str]:
    """Read and base64-encode an image file. Returns (base64_data_url, mime_type)."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {image_path}")
    if not path.is_file():
        raise ValueError(f"路径不是文件: {image_path}")

    ext = path.suffix.lower()
    if ext not in MIME_MAP:
        raise ValueError(
            f"不支持的图片格式: {ext}，支持: {list(MIME_MAP.keys())}"
        )

    file_size = path.stat().st_size
    if file_size > MAX_IMAGE_BYTES:
        raise ValueError(
            f"图片过大: {file_size / 1024 / 1024:.1f}MB，"
            f"限制 {MAX_IMAGE_BYTES / 1024 / 1024:.0f}MB"
        )
    if file_size == 0:
        raise ValueError("图片文件为空")

    mime_type = MIME_MAP[ext]
    with open(image_path, "rb") as f:
        image_data = f.read()

    base64_image = base64.b64encode(image_data).decode("utf-8")
    return f"data:{mime_type};base64,{base64_image}", mime_type


def _call_vision(
    image_url: str, prompt: str | None = None, max_tokens: int = 4096
) -> str:
    """Call the vision model and return the description text."""
    user_text = prompt or "请详细描述这张图片的内容。"

    completion = client.chat.completions.create(
        model=KIMI_MODEL,
        messages=[
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": user_text},
                ],
            },
        ],
        max_tokens=max_tokens,
    )

    return completion.choices[0].message.content


@mcp.tool()
def describe_image(
    image_path: str,
    prompt: str | None = None,
    max_tokens: int = 4096,
) -> str:
    """识别图片内容。传入本地图片的绝对路径，返回AI对图片内容的详细描述。

    参数:
    - image_path: 图片的绝对路径，支持 PNG/JPG/JPEG/GIF/WEBP/BMP
    - prompt: 自定义提示词，可指定需要提取的信息类型（如"提取所有文字"、"描述图表结构"等）
    - max_tokens: 最大输出长度，默认4096
    """
    try:
        image_url, _ = _encode_image(image_path)
        return _call_vision(image_url, prompt, max_tokens)
    except FileNotFoundError as e:
        return str(e)
    except ValueError as e:
        return str(e)


@mcp.tool()
def describe_image_to_file(
    image_path: str,
    output_path: str | None = None,
    prompt: str | None = None,
    max_tokens: int = 4096,
) -> str:
    """识别图片内容并保存到文件（解决 Windows 终端中文乱码问题）。

    将AI识别结果直接写入UTF-8编码的文本文件，完全绕过终端编码问题。
    如果未指定输出路径，默认在原图同目录下生成同名的 .md 文件。

    参数:
    - image_path: 图片的绝对路径
    - output_path: 输出文件的路径（可选，默认与原图同名 .md）
    - prompt: 自定义提示词
    - max_tokens: 最大输出长度
    """
    try:
        image_url, _ = _encode_image(image_path)
        result = _call_vision(image_url, prompt, max_tokens)

        if output_path:
            out = Path(output_path)
        else:
            img = Path(image_path)
            out = img.with_suffix(".md")

        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result, encoding="utf-8")

        return f"OK: 识别结果已保存到 {out}\n\n---\n{result}"
    except FileNotFoundError as e:
        return str(e)
    except ValueError as e:
        return str(e)


def main():
    """Entry point for CLI. Runs the MCP server via stdio."""
    import asyncio

    asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    main()
