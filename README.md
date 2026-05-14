# MCP Vision Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP server for image recognition via Kimi/Moonshot vision API. Works with **Claude Code** as a global MCP plugin — send local image paths and get AI-powered content descriptions, OCR text extraction, and more.

## Features

- **describe_image** — Recognize image content and return text description
- **describe_image_to_file** — Recognize and save result to a UTF-8 file (solves CJK terminal encoding issues on Windows)
- Supports PNG / JPG / GIF / WebP / BMP up to 20MB
- Customizable prompt for targeted extraction (e.g., "extract all Chinese text")

## Quick Start

### 1. Install

```bash
pip install mcp-vision-server
```

Or install from source:

```bash
git clone https://github.com/coffe-d/MCP-Vision-Server.git
cd mcp-vision-server
pip install -e .
```

### 2. Get a Kimi API key

Sign up at [Moonshot Platform](https://platform.moonshot.cn/console/api-keys) and create an API key.

### 3. Register with Claude Code

```bash
# Set the API key as an environment variable for the MCP server
claude mcp add vision-server \
  --env KIMI_API_KEY="sk-your-key-here" \
  -- mcp-vision-server
```

That's it. Claude Code will now have two new tools: `describe_image` and `describe_image_to_file`.

### 4. Use in Claude Code

Just mention an image path and Claude can read it:

> Please extract the text from d:\photos\handwritten-essay.jpg

## Configuration

| Environment Variable | Required | Default | Description |
|----------------------|----------|---------|-------------|
| `KIMI_API_KEY` | Yes | — | Your Moonshot API key |
| `KIMI_BASE_URL` | No | `https://api.moonshot.cn/v1` | API base URL |
| `KIMI_MODEL` | No | `moonshot-v1-8k-vision-preview` | Model name |

### Using a different vision model

```bash
claude mcp add vision-server \
  --env KIMI_API_KEY="sk-..." \
  --env KIMI_MODEL="moonshot-v1-32k-vision-preview" \
  -- mcp-vision-server
```

## API Reference

### `describe_image`

Recognize image content. Pass an absolute local image path, returns a detailed AI description.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_path` | string | Yes | — | Absolute path to image file |
| `prompt` | string | No | — | Custom prompt for targeted extraction |
| `max_tokens` | int | No | 4096 | Max output tokens |

### `describe_image_to_file`

Same as `describe_image`, but saves the result to a UTF-8 text file. Useful for CJK environments where terminal encoding may garble Chinese characters.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_path` | string | Yes | — | Absolute path to image file |
| `output_path` | string | No | auto (.md) | Output file path |
| `prompt` | string | No | — | Custom prompt |
| `max_tokens` | int | No | 4096 | Max output tokens |

## Supported Image Formats

| Format | Extension |
|--------|-----------|
| PNG | `.png` |
| JPEG | `.jpg`, `.jpeg` |
| GIF | `.gif` |
| WebP | `.webp` |
| BMP | `.bmp` |

Maximum file size: 20 MB.

## Troubleshooting

**"KIMI_API_KEY environment variable is not set"**

Make sure you passed `--env KIMI_API_KEY="sk-..."` when running `claude mcp add`, or set it in your shell profile.

**Chinese characters appear garbled in terminal output**

Use `describe_image_to_file` instead — it writes results to a UTF-8 encoded file, bypassing terminal encoding issues entirely.

**"不支持的图片格式" error**

Only PNG, JPG, JPEG, GIF, WebP, and BMP are supported. Convert your image first.

## License

MIT — see [LICENSE](./LICENSE) for details.

---

## 中文说明

MCP Vision Server 是一个基于 Kimi/Moonshot 视觉 API 的 MCP 服务器，可作为 Claude Code 的全局插件使用。

### 安装

```bash
pip install mcp-vision-server
```

### 注册到 Claude Code

```bash
claude mcp add vision-server \
  --env KIMI_API_KEY="sk-你的密钥" \
  -- mcp-vision-server
```

### 可用工具

- `describe_image` — 识别图片内容，返回文字描述
- `describe_image_to_file` — 识别并保存为 UTF-8 文件（推荐中文用户使用）

### 环境变量

| 变量 | 必填 | 默认值 |
|------|------|--------|
| `KIMI_API_KEY` | 是 | — |
| `KIMI_BASE_URL` | 否 | `https://api.moonshot.cn/v1` |
| `KIMI_MODEL` | 否 | `moonshot-v1-8k-vision-preview` |
