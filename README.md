# AI Agent 项目集合

这是一个包含多个 AI Agent 的项目集合，使用智谱和 DeepSeek API。

## 项目结构

```
├── baby-agent.py      # 计算器 Agent（智谱 API）
├── deepseek-agent.py  # DeepSeek 文字 Agent
├── image-agent.py     # 图片生成 Agent（智谱 CogView-3）
└── README.md          # 项目说明
```

## 功能说明

### 1. baby-agent.py
简易计算器 Agent，可以调用计算器工具进行数学运算。

### 2. deepseek-agent.py
使用 DeepSeek API 的文字 Agent。

### 3. image-agent.py
图片生成工具，支持：
- 命令行模式
- Gradio 可视化界面
- 多种图片尺寸选择
- 自动保存到 generated_images 文件夹

## 使用方法

### 安装依赖

```bash
pip install openai requests pillow gradio
```

### 设置环境变量

```powershell
# 智谱 API Key
$env:ZHIPU_API_KEY = "你的智谱密钥"

# DeepSeek API Key（可选）
$env:DEEPSEEK_API_KEY = "你的DeepSeek密钥"
```

### 运行

```bash
# 计算器 Agent
python baby-agent.py

# DeepSeek Agent
python deepseek-agent.py

# 图片生成 Agent（命令行模式）
python image-agent.py

# 图片生成 Agent（Gradio界面）
python image-agent.py --gui
```

## API Key 获取

- 智谱 API: https://open.bigmodel.cn/
- DeepSeek API: https://platform.deepseek.com/

## 注意事项

- 图片生成 API 是收费服务，请留意费用
- 建议使用环境变量管理 API Key，不要硬编码