import streamlit as st

from frontend.ui_components import show_sidebar, show_footer, apply_common_styles, display_project_info

# Apply custom styles
apply_common_styles()

# Display sidebar
show_sidebar()


def main():
    st.title("🚀 LLM-TextKit")
    
    display_project_intro()
    
    # Display project information
    display_project_info()

    st.markdown("---")

    display_feature_overview()
    display_project_highlights()
    display_documentation_link()

    # Footer
    show_footer()


def display_project_intro():
    st.info(
        """
        LLM-TextKit 是一个基于大语言模型的文本分析平台，专注于提供高效、准确的文本处理解决方案。
        
        该工具集提供情感分析、文本聚类和智能翻译三大核心功能，帮助用户快速理解和处理大量文本数据。
        """
    )


def display_feature_overview():
    st.markdown("## 功能概览")

    features = [
        ("🏷️ 情感分析与标注", "基于大语言模型的文本内容分析，支持有效性判断、情感倾向分析和敏感信息识别"),
        ("🗂️ 文本聚类分析", "自动提炼大量文本中的话题模式，支持单标签和多标签分类"),
        ("🌐 智能语境翻译", "结合上下文理解的高质量多语言翻译，自动检测语言并批量处理"),
    ]

    cols = st.columns(3)
    for i, (icon, desc) in enumerate(features):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"##### {icon}")
                st.markdown(desc)


def display_project_highlights():
    st.markdown("## 项目亮点")
    st.markdown(
        """
        - **强大的AI能力**: 基于先进的大语言模型，提供准确的文本理解和处理能力
        - **批量处理**: 支持大规模文本数据的批量处理，显著提升工作效率
        - **灵活配置**: 可自定义分类类别、上下文背景等参数，适应不同场景需求
        - **实时监控**: 集成 Langfuse 监控，提供详细的处理过程追踪和性能分析
        - **用户友好**: 简洁直观的界面设计，支持CSV文件上传和结果下载
        """
    )


def display_documentation_link():
    st.markdown("## 使用指南")

    st.markdown(
        """
        ### Quick Start
        
        1. **情感分析与标注**: 分析文本的有效性、情感倾向和敏感信息
        2. **文本聚类分析**: 自动发现文本中的主题并进行分类
        3. **智能语境翻译**: 批量翻译文本，支持上下文理解
        
        请从左侧菜单选择相应功能开始使用。
        """
    )


main()
