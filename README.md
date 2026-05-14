# MCP Vision Server · 视觉识别服务

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**语言 / Language：** [中文](#中文) | [English](#english)

基于 Kimi/Moonshot 视觉 API 的 MCP 服务器，作为 Claude Code 全局插件使用。传入本地图片路径，返回 AI 对图片内容的详细描述、文字提取等。

MCP server for image recognition via Kimi/Moonshot vision API. Works as a global Claude Code plugin.

---

## 中文

### 功能

- **describe_image** — 识别图片内容，返回文字描述
- **describe_image_to_file** — 识别并保存为 UTF-8 文件（解决 Windows 终端中文乱码）
- 支持 PNG / JPG / GIF / WebP / BMP，最大 20MB
- 支持自定义提示词（如"提取所有文字""描述图表结构"）

### 安装

```bash
pip install mcp-vision-server
```

或从源码安装：

```bash
git clone https://github.com/coffe-d/MCP-Vision-Server.git
cd mcp-vision-server
pip install -e .
```

### 获取 API Key

在 [Moonshot 开放平台](https://platform.moonshot.cn/console/api-keys) 注册并创建 API Key。

### 注册到 Claude Code

```bash
claude mcp add vision-server \
  --env KIMI_API_KEY="sk-你的密钥" \
  -- mcp-vision-server
```

注册后 Claude Code 即可使用 `describe_image` 和 `describe_image_to_file` 两个工具。

### 配置

| 环境变量 | 必填 | 默认值 | 说明 |
|----------|------|--------|------|
| `KIMI_API_KEY` | 是 | — | Moonshot API 密钥 |
| `KIMI_BASE_URL` | 否 | `https://api.moonshot.cn/v1` | API 地址 |
| `KIMI_MODEL` | 否 | `moonshot-v1-8k-vision-preview` | 模型名称 |

### 工具说明

**describe_image** — 识别图片，返回文本描述。

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `image_path` | string | 是 | — | 图片绝对路径 |
| `prompt` | string | 否 | — | 自定义提示词 |
| `max_tokens` | int | 否 | 4096 | 最大输出长度 |

**describe_image_to_file** — 识别图片，结果保存为 UTF-8 文件。适合中文环境避免终端乱码。

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `image_path` | string | 是 | — | 图片绝对路径 |
| `output_path` | string | 否 | 自动（同名 .md） | 输出文件路径 |

### 常见问题

**"KIMI_API_KEY environment variable is not set"**

未设置环境变量。注册时确保使用了 `--env KIMI_API_KEY="sk-..."`。

**终端中文乱码**

使用 `describe_image_to_file` 代替 `describe_image`，结果直接写入 UTF-8 文件。

**"不支持的图片格式"**

仅支持 PNG、JPG、JPEG、GIF、WebP、BMP 格式。

### 许可

MIT — 详见 [LICENSE](./LICENSE)。

---

## English

### Features

- **describe_image** — Recognize image content and return text description
- **describe_image_to_file** — Recognize and save result to a UTF-8 file
- Supports PNG / JPG / GIF / WebP / BMP up to 20MB
- Customizable prompt for targeted extraction

### Install

```bash
pip install mcp-vision-server
```

Or from source:

```bash
git clone https://github.com/coffe-d/MCP-Vision-Server.git
cd mcp-vision-server
pip install -e .
```

### Get an API key

Sign up at [Moonshot Platform](https://platform.moonshot.cn/console/api-keys) and create an API key.

### Register with Claude Code

```bash
claude mcp add vision-server \
  --env KIMI_API_KEY="sk-your-key-here" \
  -- mcp-vision-server
```

### Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `KIMI_API_KEY` | Yes | — | Moonshot API key |
| `KIMI_BASE_URL` | No | `https://api.moonshot.cn/v1` | API base URL |
| `KIMI_MODEL` | No | `moonshot-v1-8k-vision-preview` | Model name |

### API Reference

**describe_image** — Return image description as text.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_path` | string | Yes | — | Absolute path to image |
| `prompt` | string | No | — | Custom prompt |
| `max_tokens` | int | No | 4096 | Max output tokens |

**describe_image_to_file** — Save result to a UTF-8 file.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_path` | string | Yes | — | Absolute path to image |
| `output_path` | string | No | auto (.md) | Output file path |

### Troubleshooting

**"KIMI_API_KEY environment variable is not set"** — Make sure you passed `--env KIMI_API_KEY="sk-..."` when running `claude mcp add`.

**Garbled Chinese in terminal** — Use `describe_image_to_file` to write directly to UTF-8 file.

### License

MIT — see [LICENSE](./LICENSE).
