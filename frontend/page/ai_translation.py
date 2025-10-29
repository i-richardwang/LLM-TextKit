import asyncio
import os
import uuid
import re
from typing import List

import pandas as pd
import streamlit as st
from asyncio import Semaphore

from frontend.ui_components import show_sidebar, show_footer, apply_common_styles, display_project_info
from backend.translation.translator import Translator

# Apply custom styles
apply_common_styles()

# Display sidebar
show_sidebar()

# Initialize translator
translator = Translator()

# Initialize session state
if "translation_results" not in st.session_state:
    st.session_state.translation_results = None
if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None


def contains_chinese(text: str) -> bool:
    """
    Check if text contains more than 50% Chinese characters.

    Args:
        text (str): Text to check.

    Returns:
        bool: Returns True if text contains more than 50% Chinese characters; otherwise False.
    """
    if isinstance(text, str):
        chinese_chars = re.findall("[\u4e00-\u9fff]", text)
        return len(chinese_chars) / len(text) >= 0.5 if text else False
    return False


async def translate_text(text: str, text_topic: str) -> str:
    """
    Asynchronously translate a single text, returning original text if it's primarily Chinese.

    Args:
        text (str): Text to translate.
        text_topic (str): Text topic.

    Returns:
        str: Translated text, original Chinese text, or error message.
    """
    try:
        if contains_chinese(text):
            return text  # If text is primarily Chinese, return original
        session_id = str(uuid.uuid4())
        return await translator.translate(text, text_topic, session_id)
    except Exception as e:
        return f"翻译错误: {str(e)}"


async def batch_translate(
    texts: List[str], text_topic: str, session_id: str, max_concurrent: int = 3
) -> List[str]:
    """
    Batch translate texts with concurrency limit, skipping primarily Chinese texts.

    Args:
        texts (List[str]): List of texts to translate.
        text_topic (str): Text topic.
        session_id (str): Session ID for the entire CSV file.
        max_concurrent (int): Maximum concurrent translations, defaults to 3.

    Returns:
        List[str]: List of translated texts.
    """
    semaphore = Semaphore(max_concurrent)

    async def translate_with_semaphore(text: str) -> str:
        async with semaphore:
            if contains_chinese(text):
                return text  # If text is primarily Chinese, return original
            return await translator.translate(text, text_topic, session_id)

    tasks = [translate_with_semaphore(text) for text in texts]
    return await asyncio.gather(*tasks)


def display_translation_info() -> None:
    """Display introduction information for translation feature."""
    st.info(
        """
    智能语境翻译是一个高效的多语言翻译工具，专为批量处理文本设计，通过上下文理解提高翻译准确性。
    本工具会自动检测并跳过主要由中文组成的文本，只翻译非中文文本。

    智能语境翻译适用于需要快速、准确翻译大量文本的各类场景，如多语言数据分析。
    """
    )


def perform_translation(
    df: pd.DataFrame, text_column: str, text_topic: str, max_concurrent: int = 3
) -> pd.DataFrame:
    """
    Perform batch translation.

    Args:
        df (pd.DataFrame): DataFrame containing texts to translate.
        text_column (str): Name of text column to translate.
        text_topic (str): Text topic.
        max_concurrent (int): Maximum concurrent translations, defaults to 3.

    Returns:
        pd.DataFrame: DataFrame containing translation results.
    """
    texts_to_translate = df[text_column].tolist()
    session_id = str(uuid.uuid4())
    translated_texts = []

    async def translate_and_save(texts: List[str]) -> List[str]:
        results = await batch_translate(texts, text_topic, session_id, max_concurrent)
        translated_texts.extend(results)

        # Save temporary results every 10 translations
        if len(translated_texts) % 10 == 0 or len(translated_texts) == len(
            texts_to_translate
        ):
            temp_df = df.copy()
            temp_df["translated_text"] = translated_texts + [""] * (
                len(df) - len(translated_texts)
            )
            save_temp_results(temp_df, session_id)

        return results

    with st.spinner("正在批量翻译..."):
        asyncio.run(translate_and_save(texts_to_translate))

    df["translated_text"] = translated_texts
    return df


def save_temp_results(df: pd.DataFrame, session_id: str) -> None:
    """
    Save temporary translation results to CSV file.

    Args:
        df (pd.DataFrame): DataFrame containing translation results.
        session_id (str): Session ID for generating unique filename.
    """
    temp_dir = os.path.join("data", "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, f"translation_results_{session_id}.csv")
    df.to_csv(temp_file_path, index=False, encoding="utf-8-sig")


def display_translation_results(translation_results: pd.DataFrame) -> None:
    """
    Display translation results.

    Args:
        translation_results (pd.DataFrame): DataFrame containing translation results.
    """
    st.markdown("## 翻译结果")
    with st.container(border=True):
        if isinstance(translation_results, dict):
            with st.expander("查看翻译结果", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("原文")
                    st.markdown(translation_results["original"])
                with col2:
                    st.subheader("译文")
                    st.markdown(translation_results["translated"])
        elif isinstance(translation_results, pd.DataFrame):
            st.dataframe(translation_results)
            csv = translation_results.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="下载翻译结果CSV",
                data=csv,
                file_name="translated_results.csv",
                mime="text/csv",
            )


def main() -> None:
    """Main function containing the entire intelligent contextual translation workflow."""
    st.title("🌐 智能语境翻译")

    # Display feature introduction
    display_translation_info()
    
    # Display project information
    display_project_info()
    
    st.markdown("---")

    st.markdown("## 文本翻译")

    with st.container(border=True):
        text_topic = st.text_input(
            "请输入文本主题", placeholder="例如：员工反馈、绩效评价、工作报告等"
        )

        tab1, tab2 = st.tabs(["直接输入", "上传CSV文件"])

        with tab1:
            with st.form("single_translation_form", border=False):
                text_to_translate = st.text_area("请输入要翻译的文本", height=150)
                submit_button = st.form_submit_button("翻译")

                if submit_button and text_to_translate and text_topic:
                    if contains_chinese(text_to_translate):
                        st.info("检测到输入的文本主要是中文，无需翻译。")
                        st.session_state.translation_results = {
                            "original": text_to_translate,
                            "translated": text_to_translate,
                        }
                    else:
                        with st.spinner("正在翻译..."):
                            translated_text = asyncio.run(
                                translate_text(text_to_translate, text_topic)
                            )
                        st.session_state.translation_results = {
                            "original": text_to_translate,
                            "translated": translated_text,
                        }

        with tab2:
            uploaded_file = st.file_uploader("上传CSV文件", type="csv")
            
            if st.button("📥 导入示例数据", key="demo_data_translation"):
                try:
                    demo_path = os.path.join(os.path.dirname(__file__), "..", "demo_data", "demo_texts.csv")
                    st.session_state.uploaded_df = pd.read_csv(demo_path)
                    st.success("✅ 已加载示例数据")
                except Exception as e:
                    st.error(f"❌ 加载示例数据失败：{str(e)}")
            
            # Process uploaded file
            if uploaded_file is not None:
                try:
                    st.session_state.uploaded_df = pd.read_csv(uploaded_file)
                except Exception as e:
                    st.error(f"处理CSV文件时出错：{str(e)}")
            
            # If data is loaded (either via upload or sample data), display operation interface
            if st.session_state.uploaded_df is not None:
                st.write("预览上传的数据：")
                st.dataframe(st.session_state.uploaded_df)
                
                text_column = st.selectbox("选择包含要翻译文本的列", st.session_state.uploaded_df.columns)
                
                if st.button("开始批量翻译") and text_topic:
                    st.session_state.translation_results = perform_translation(
                        st.session_state.uploaded_df, text_column, text_topic
                    )

    if st.session_state.translation_results is not None:
        display_translation_results(st.session_state.translation_results)

    # Footer
    show_footer()


main()
