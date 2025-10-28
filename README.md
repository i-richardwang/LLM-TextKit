# LLM-TextKit

[中文](./README_zh.md) | **English**

An intelligent text analysis platform powered by Large Language Models, providing three core features: sentiment analysis, text clustering, and intelligent translation.

## Features

### 🏷️ Sentiment Analysis & Annotation

AI-powered text content analysis tool with support for:
- **Validity Assessment**: Automatically identify invalid or low-quality text content
- **Sentiment Classification**: Classify text as positive, neutral, or negative sentiment
- **Sensitive Information Detection**: Detect whether text contains sensitive information

**Use Cases**:
- User feedback analysis
- Social media monitoring
- Customer review analysis
- Employee survey analysis

### 🗂️ Text Clustering Analysis

Leveraging the semantic understanding capabilities of Large Language Models to automatically identify and categorize main topics from large volumes of text:
- **Auto Clustering**: System automatically discovers topics and generates categories
- **Custom Categories**: Support for user-defined classification categories
- **Single/Multi-label Classification**: Flexible choice between single-label or multi-label classification
- **Batch Processing**: Efficient processing of large-scale text data

**Use Cases**:
- User feedback topic categorization
- Topic trend analysis
- Content classification and organization
- Public opinion analysis

### 🌐 Intelligent Contextual Translation

High-quality multilingual translation tool with contextual understanding:
- **Context Understanding**: More accurate translation based on text topic
- **Batch Processing**: Support for CSV file batch translation
- **Smart Detection**: Automatically detect and skip Chinese text
- **Async Processing**: Concurrent translation for improved processing efficiency

**Use Cases**:
- Multilingual data analysis
- Internationalized content processing
- Cross-language document translation

## Quick Start

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/i-richardwang/LLM-TextKit.git
cd LLM-TextKit

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file and configure the following environment variables:

```bash
# OpenAI API Configuration
# Compatible with OpenAI or any service using OpenAI API format

OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4

# Langfuse Monitoring Configuration (Optional)
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

**Notes**:
- Supports any service compatible with OpenAI API format (OpenAI, DeepSeek, SiliconCloud, etc.)
- Simply modify `OPENAI_BASE_URL` and `OPENAI_MODEL_NAME` to switch between different services
- Langfuse configuration is optional, used for monitoring and tracking LLM calls

**Common Service Configuration Examples**:
```bash
# Official OpenAI
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4

# DeepSeek
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL_NAME=deepseek-chat

# SiliconCloud
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_MODEL_NAME=Qwen/Qwen2-72B-Instruct
```

### 3. Launch Application

```bash
streamlit run frontend/app.py
```

The application will automatically open in your browser, default address is `http://localhost:8501`

## Deployment

### Streamlit Cloud

1. Push code to GitHub repository
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository, set main file to `frontend/app.py`
4. Add environment variables in Settings > Secrets (refer to `secrets.toml.example`)
5. Deployment complete!

Streamlit Cloud will automatically read dependencies from `requirements.txt`.

## User Guide

### Sentiment Analysis & Annotation

1. Select "Sentiment Analysis & Annotation" from the left menu
2. Enter text context or topic
3. Choose input method:
   - **Direct Input**: Enter single text for analysis
   - **Upload CSV**: Batch process multiple texts
4. View analysis results and download

### Text Clustering Analysis

1. Select "Text Clustering Analysis" from the left menu
2. Enter text topic and additional requirements
3. Upload CSV file containing texts
4. Choose classification method (single-label/multi-label)
5. Choose clustering method:
   - **Auto Clustering**: System automatically generates categories
   - **Custom Categories**: Manually define classification categories
6. Review and edit generated categories
7. Start text classification and download results

### Intelligent Contextual Translation

1. Select "Intelligent Contextual Translation" from the left menu
2. Enter text topic
3. Choose input method:
   - **Direct Input**: Translate single text
   - **Upload CSV**: Batch translate multiple texts
4. View translation results and download

## Project Structure

```
AI_HR_Demo/
├── backend/                       # Backend core functionality
│   ├── classification/            # Sentiment analysis & annotation
│   ├── clustering/                # Text clustering
│   └── translation/               # Intelligent translation
├── frontend/                      # Frontend interface
│   ├── page/                      # Feature pages
│   │   ├── sentiment_analysis.py # Sentiment analysis page
│   │   ├── text_clustering.py    # Text clustering page
│   │   └── ai_translation.py     # Translation page
│   ├── Home.py                    # Home page
│   ├── app.py                     # Application entry point
│   └── ui_components.py           # UI components
├── utils/                         # Utility functions
│   ├── llm_tools.py              # LLM tools
│   └── text_utils.py             # Text processing utilities
├── data/                          # Data directory
│   ├── llm_cache/                # LLM cache
│   ├── temp/                     # Temporary files
│   └── results/                  # Result files
├── .streamlit/                    # Streamlit configuration
│   └── config.toml               # Streamlit config file
├── pyproject.toml                 # UV project configuration
├── uv.lock                        # UV dependency lock file
├── secrets.toml.example          # Streamlit Cloud config template
└── README.md                     # Project documentation
```

## Tech Stack

- **Dependency Management**: UV
- **Python Version**: 3.12+
- **AI Framework**: LangChain, OpenAI SDK
- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Monitoring**: Langfuse (optional)
- **Async Processing**: asyncio, aiohttp

## Compatibility

This project uses OpenAI SDK and supports all services compatible with OpenAI API format, including but not limited to:
- Official OpenAI API
- DeepSeek
- SiliconCloud
- Azure OpenAI
- Other local or cloud services compatible with OpenAI API

## Notes

1. **API Key Security**: Do not commit API keys to version control
2. **Data Privacy**: Ensure compliance with relevant regulations when processing sensitive data
3. **Cost Control**: Batch processing large volumes of text may incur high API costs
4. **Performance Optimization**: Adjust concurrency and batch size based on actual needs

## Contributing

Issues and Pull Requests are welcome to improve the project.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Disclaimer

This project is in experimental stage and is primarily for learning and research purposes. Use with caution in production environments and assume your own risks.

## Contact

For questions or suggestions, please contact:
- Email: contact@xmail.ing
- GitHub: https://github.com/i-richardwang/LLM-TextKit

