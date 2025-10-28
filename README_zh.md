# LLM-TextKit

**中文** | [English](./README.md)

基于大语言模型的智能文本分析平台，提供情感分析、文本聚类和智能翻译三大核心功能。

## 功能特性

### 🏷️ 情感分析与标注

基于大语言模型的文本内容分析工具，支持：
- **有效性判断**：自动识别无效或低质量的文本内容
- **情感倾向分析**：将文本分类为正向、中性或负向情感
- **敏感信息识别**：检测文本中是否包含敏感信息

**适用场景**：
- 用户反馈分析
- 社交媒体监控
- 客户评论分析
- 员工调研分析

### 🗂️ 文本聚类分析

利用大语言模型的语义理解能力，自动化地从大量文本中识别和归类主要主题：
- **自动聚类**：系统自动发现文本中的主题并生成类别
- **自定义类别**：支持用户自定义分类类别
- **单/多标签分类**：灵活选择单标签或多标签分类方式
- **批量处理**：高效处理大规模文本数据

**适用场景**：
- 用户反馈主题归类
- 话题趋势分析
- 内容分类整理
- 舆情分析

### 🌐 智能语境翻译

结合上下文理解的高质量多语言翻译工具：
- **上下文理解**：基于文本主题提供更准确的翻译
- **批量处理**：支持CSV文件批量翻译
- **智能检测**：自动检测并跳过中文文本
- **异步处理**：并发翻译提升处理效率

**适用场景**：
- 多语言数据分析
- 国际化内容处理
- 跨语言文档翻译

## 快速开始

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/i-richardwang/LLM-TextKit.git
cd LLM-TextKit

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件并配置以下环境变量：

```bash
# OpenAI API Configuration
# 适用于 OpenAI 或任何兼容 OpenAI API 格式的服务

OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4

# Langfuse监控配置（可选）
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

**说明**：
- 支持任何兼容 OpenAI API 格式的服务（OpenAI、DeepSeek、SiliconCloud 等）
- 只需修改 `OPENAI_BASE_URL` 和 `OPENAI_MODEL_NAME` 即可切换不同的服务
- Langfuse 配置为可选项，用于监控和追踪 LLM 调用

**常用服务配置示例**：
```bash
# OpenAI 官方
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4

# DeepSeek
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL_NAME=deepseek-chat

# SiliconCloud
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_MODEL_NAME=Qwen/Qwen2-72B-Instruct
```

### 3. 启动应用

```bash
streamlit run frontend/app.py
```

应用将在浏览器中自动打开，默认地址为 `http://localhost:8501`

## 部署

### Streamlit Cloud

1. 将代码推送到 GitHub 仓库
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 连接你的 GitHub 仓库，主文件设置为 `frontend/app.py`
4. 在 Settings > Secrets 中添加环境变量（参考 `secrets.toml.example`）
5. 部署完成！

Streamlit Cloud 会自动从 `requirements.txt` 读取依赖。

## 使用指南

### 情感分析与标注

1. 在左侧菜单选择 "情感分析与标注"
2. 输入文本的上下文或主题
3. 选择输入方式：
   - **直接输入**：输入单条文本进行分析
   - **上传CSV**：批量处理多条文本
4. 查看分析结果并下载

### 文本聚类分析

1. 在左侧菜单选择 "文本聚类分析"
2. 输入文本主题和补充要求
3. 上传包含文本的CSV文件
4. 选择分类方式（单标签/多标签）
5. 选择聚类方式：
   - **自动聚类**：系统自动生成类别
   - **自定义类别**：手动定义分类类别
6. 审核并编辑生成的类别
7. 开始文本分类并下载结果

### 智能语境翻译

1. 在左侧菜单选择 "智能语境翻译"
2. 输入文本主题
3. 选择输入方式：
   - **直接输入**：翻译单条文本
   - **上传CSV**：批量翻译多条文本
4. 查看翻译结果并下载

## 项目结构

```
AI_HR_Demo/
├── backend/                       # 后端核心功能
│   ├── classification/            # 情感分析与标注
│   ├── clustering/                # 文本聚类
│   └── translation/               # 智能翻译
├── frontend/                      # 前端界面
│   ├── page/                      # 功能页面
│   │   ├── sentiment_analysis.py # 情感分析页面
│   │   ├── text_clustering.py    # 文本聚类页面
│   │   └── ai_translation.py     # 翻译页面
│   ├── Home.py                    # 主页
│   ├── app.py                     # 应用入口
│   └── ui_components.py           # UI组件
├── utils/                         # 工具函数
│   ├── llm_tools.py              # LLM工具
│   └── text_utils.py             # 文本处理工具
├── data/                          # 数据目录
│   ├── llm_cache/                # LLM缓存
│   ├── temp/                     # 临时文件
│   └── results/                  # 结果文件
├── .streamlit/                    # Streamlit配置
│   └── config.toml               # Streamlit配置文件
├── pyproject.toml                 # UV 项目配置
├── uv.lock                        # UV 依赖锁定文件
├── secrets.toml.example          # Streamlit Cloud 配置模板
└── README.md                     # 项目文档
```

## 技术栈

- **依赖管理**: UV
- **Python版本**: 3.12+
- **AI框架**: LangChain, OpenAI SDK
- **前端**: Streamlit
- **数据处理**: Pandas
- **监控**: Langfuse（可选）
- **异步处理**: asyncio, aiohttp

## 兼容性说明

本项目使用 OpenAI SDK，支持所有兼容 OpenAI API 格式的服务，包括但不限于：
- OpenAI 官方 API
- DeepSeek
- SiliconCloud
- Azure OpenAI
- 其他兼容 OpenAI API 的本地或云端服务

## 注意事项

1. **API密钥安全**：请勿将API密钥提交到版本控制系统
2. **数据隐私**：处理敏感数据时请确保符合相关法规
3. **成本控制**：批量处理大量文本可能产生较高的API调用费用
4. **性能优化**：建议根据实际情况调整并发数和批次大小

## 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 许可

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

## 免责声明

本项目处于实验阶段，主要用于学习和研究目的。在实际应用中使用时请谨慎，并自行承担相关风险。

## 联系方式

如有问题或建议，请通过以下方式联系：
- Email: contact@xmail.ing
- GitHub: https://github.com/i-richardwang/LLM-TextKit
