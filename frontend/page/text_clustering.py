import streamlit as st
import pandas as pd
import uuid
import os
from typing import Dict

from frontend.ui_components import show_sidebar, show_footer, apply_common_styles, display_project_info
from backend.clustering.clustering_workflow import (
    generate_categories,
    classify_texts,
)

# Apply custom styles
apply_common_styles()

# Display sidebar
show_sidebar()


def initialize_session_state():
    """Initialize session state variables"""
    session_vars = [
        "df_preprocessed",
        "categories",
        "df_result",
        "text_column",
        "text_topic",
        "session_id",
        "clustering_params",
        "use_custom_categories",
        "additional_requirements",
        "is_multi_label",
    ]
    for var in session_vars:
        if var not in st.session_state:
            st.session_state[var] = None

    if st.session_state.session_id is None:
        st.session_state.session_id = str(uuid.uuid4())

    if st.session_state.clustering_params is None:
        st.session_state.clustering_params = {
            "min_categories": 5,
            "max_categories": 8,
            "batch_size": 10,
            "classification_batch_size": 10,
        }

    if st.session_state.use_custom_categories is None:
        st.session_state.use_custom_categories = False

    if st.session_state.additional_requirements is None:
        st.session_state.additional_requirements = None

    if st.session_state.is_multi_label is None:
        st.session_state.is_multi_label = False


def display_info_message():
    """Display information message for text clustering analysis tool"""
    st.info(
        """
        文本聚类分析工具利用大语言模型的语义理解能力，自动化地从大量文本中识别和归类主要主题。
        
        适用于各类文本内容分析场景，如用户反馈归类、话题趋势分析等。
        
        现在支持单标签和多标签分类，可以根据需求选择合适的分类方式。
        """
    )


def display_workflow_introduction():
    """Display workflow introduction"""
    with st.expander("📋 查看文本聚类分析使用说明", expanded=False):
        st.markdown(
            """
            1. 上传数据：准备包含文本数据的CSV文件，并上传到系统。
            2. 设置参数：选择文本列，输入主题背景，设置聚类参数。
            3. 选择分类方式：选择单标签或多标签分类。
            4. 初始聚类：系统自动进行初始聚类，生成类别。
            5. 审核类别：查看并编辑生成的类别，确保符合需求。
            6. 文本分类：对所有文本进行分类。
            7. 查看结果：浏览分类结果，下载分析报告。
            """
        )


def get_clustering_parameters():
    """Get and update clustering parameter settings"""
    with st.expander("自动聚类参数设置"):
        st.session_state.clustering_params["min_categories"] = st.slider(
            "最小类别数量",
            5,
            15,
            st.session_state.clustering_params.get("min_categories", 10),
            key="min_categories_slider",
        )
        st.session_state.clustering_params["max_categories"] = st.slider(
            "最大类别数量",
            st.session_state.clustering_params["min_categories"],
            20,
            st.session_state.clustering_params.get("max_categories", 15),
            key="max_categories_slider",
        )
        st.session_state.clustering_params["batch_size"] = st.slider(
            "聚类批处理大小",
            10,
            1000,
            st.session_state.clustering_params.get("batch_size", 100),
            key="batch_size_slider",
        )
        st.session_state.clustering_params["classification_batch_size"] = st.slider(
            "分类批处理大小",
            10,
            100,
            st.session_state.clustering_params.get(
                "classification_batch_size", 20),
            key="classification_batch_size_slider",
        )


def get_custom_classification_parameters():
    """Get and update custom classification parameter settings"""
    with st.expander("自定义类别分类参数设置"):
        st.session_state.clustering_params["classification_batch_size"] = st.slider(
            "分类批处理大小",
            10,
            100,
            st.session_state.clustering_params.get(
                "classification_batch_size", 20),
            key="custom_classification_batch_size_slider",
        )


def handle_data_input_and_clustering():
    """Handle data input and initial clustering process"""
    st.markdown("## 数据输入和聚类设置")

    with st.container(border=True):
        st.session_state.text_topic = st.text_input(
            "请输入文本主题或背景",
            value=st.session_state.text_topic if st.session_state.text_topic else "",
            placeholder="例如：员工反馈、产品评论、客户意见等",
        )

        st.session_state.additional_requirements = st.text_area(
            "补充要求（可选）",
            value=(
                st.session_state.additional_requirements
                if st.session_state.additional_requirements
                else ""
            ),
            placeholder="例如：忽略员工对于薪酬福利的抱怨",
        )

        uploaded_file = st.file_uploader("上传CSV文件", type="csv")
        
        if st.button("📥 导入示例数据"):
            try:
                demo_path = os.path.join(os.path.dirname(__file__), "..", "demo_data", "demo_texts.csv")
                df = pd.read_csv(demo_path)
                df["unique_id"] = [f"ID{i:06d}" for i in range(1, len(df) + 1)]
                st.session_state.df_preprocessed = df
                st.success("✅ 已加载示例数据")
            except Exception as e:
                st.error(f"❌ 加载示例数据失败：{str(e)}")
        
        # Process uploaded file
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            df["unique_id"] = [f"ID{i:06d}" for i in range(1, len(df) + 1)]
            st.session_state.df_preprocessed = df

        # If data is loaded (via upload or sample), show the operation interface
        if st.session_state.df_preprocessed is not None:
            df = st.session_state.df_preprocessed
            st.write("预览上传的数据：")
            st.dataframe(df, height=250)
            st.session_state.text_column = st.selectbox("选择包含文本的列", df.columns)

            # Select single-label or multi-label classification
            st.session_state.is_multi_label = st.radio(
                "选择分类方式",
                [False, True],
                format_func=lambda x: "多标签分类" if x else "单标签分类",
            )

            previous_use_custom_categories = st.session_state.get(
                "use_custom_categories", False
            )
            st.session_state.use_custom_categories = (
                st.radio(
                    "选择聚类方式",
                    ["自动聚类", "使用自定义类别"],
                    format_func=lambda x: (
                        "自动聚类" if x == "自动聚类" else "使用自定义类别"
                    ),
                )
                == "使用自定义类别"
            )

            # Check if clustering method has been switched
            if st.session_state.use_custom_categories != previous_use_custom_categories:
                # Reset clustering_params to default values
                st.session_state.clustering_params = {
                    "min_categories": 5,
                    "max_categories": 8,
                    "batch_size": 10,
                    "classification_batch_size": 10,
                }

            if st.session_state.use_custom_categories:
                get_custom_classification_parameters()
            else:
                get_clustering_parameters()

            if st.session_state.use_custom_categories:
                st.info("请在下方设置自定义类别")
            else:
                if st.button("开始初始聚类"):
                    with st.spinner("正在进行初始聚类..."):
                        try:
                            result = generate_categories(
                                df=df,
                                text_column=st.session_state.text_column,
                                text_topic=st.session_state.text_topic,
                                initial_category_count=st.session_state.clustering_params[
                                    "max_categories"
                                ],
                                min_categories=st.session_state.clustering_params[
                                    "min_categories"
                                ],
                                max_categories=st.session_state.clustering_params[
                                    "max_categories"
                                ],
                                batch_size=st.session_state.clustering_params[
                                    "batch_size"
                                ],
                                session_id=st.session_state.session_id,
                                additional_requirements=(
                                    f"补充要求：\n{
                                        st.session_state.additional_requirements}"
                                    if st.session_state.additional_requirements
                                    and st.session_state.additional_requirements.strip()
                                    else ""
                                ),
                            )

                            st.success("初始聚类完成！")

                            # Save results to session state
                            st.session_state.df_preprocessed = result["preprocessed_df"]
                            st.session_state.categories = result["categories"][
                                "categories"
                            ]
                        except Exception as e:
                            st.error(f"初始聚类过程中发生错误：{str(e)}")

            # Keep the processed df_preprocessed from upstream, don't overwrite with original df

        else:
            st.warning("请上传CSV文件")


def handle_custom_categories():
    """Handle user-defined custom categories input"""
    if (
        st.session_state.use_custom_categories
        and st.session_state.df_preprocessed is not None
    ):
        st.markdown("## 自定义类别输入")
        with st.container(border=True):
            custom_category_method = st.radio(
                "选择自定义类别的方式",
                ["上传CSV文件", "手动输入"],
                format_func=lambda x: (
                    "上传CSV文件" if x == "上传CSV文件" else "手动输入"
                ),
            )

            if custom_category_method == "上传CSV文件":
                uploaded_categories = st.file_uploader(
                    "上传包含自定义类别的CSV文件", type="csv"
                )
                if uploaded_categories is not None:
                    categories_df = pd.read_csv(uploaded_categories)
                    st.session_state.categories = categories_df.to_dict(
                        "records")
                    st.success("自定义类别已成功上传！")
            else:
                categories_text = st.text_area(
                    "请输入自定义类别（每行一个类别，格式：类别名称,类别描述）",
                    height=200,
                    placeholder="工作环境,描述员工对公司工作环境的感受，包括舒适度、设备和软件的先进性等。\n"
                    "薪资与福利,讨论员工对薪资水平和福利待遇的看法，包括与行业水平的比较、提升空间和健康保险等。",
                )
                if categories_text:
                    categories_list = [
                        line.split(",", 1)
                        for line in categories_text.split("\n")
                        if line.strip()
                    ]
                    categories_df = pd.DataFrame(
                        categories_list, columns=["name", "description"]
                    )
                    st.session_state.categories = categories_df.to_dict(
                        "records")
                    st.success("自定义类别已成功添加！")


def review_clustering_results():
    """Review clustering results and allow user modification"""
    if st.session_state.categories is not None:
        st.markdown("---")
        st.markdown("## 聚类结果审核")

        with st.container(border=True):
            st.markdown("请审核并根据需要修改、添加或删除类别：")

            # Convert category list to DataFrame for use with st.data_editor
            categories_df = pd.DataFrame(st.session_state.categories)[
                ["name", "description"]
            ]

            # Use st.data_editor to display and edit categories
            edited_df = st.data_editor(
                categories_df,
                num_rows="dynamic",
                column_config={
                    "name": st.column_config.TextColumn(
                        "类别名称",
                        help="简洁明了的类别标签",
                        max_chars=50,
                        required=True,
                    ),
                    "description": st.column_config.TextColumn(
                        "类别描述",
                        help="详细描述该类别的特征及与其他类别的区别",
                        max_chars=200,
                        required=True,
                    ),
                },
            )

            # Convert edited DataFrame back to category list
            edited_categories = edited_df.to_dict("records")

            if st.button("确认类别并开始文本分类"):
                if st.session_state.clustering_params is None:
                    st.error("请先设置聚类参数")
                else:
                    with st.spinner("正在进行文本分类..."):
                        try:
                            df_result = classify_texts(
                                df=st.session_state.df_preprocessed,
                                text_column=st.session_state.text_column,
                                id_column="unique_id",
                                categories={"categories": edited_categories},
                                text_topic=st.session_state.text_topic,
                                session_id=st.session_state.session_id,
                                classification_batch_size=st.session_state.clustering_params[
                                    "classification_batch_size"
                                ],
                                is_multi_label=st.session_state.is_multi_label,
                            )

                            st.session_state.df_result = df_result
                            st.success("文本分类完成！")
                        except Exception as e:
                            st.error(f"文本分类过程中发生错误：{str(e)}")


def display_classification_results():
    """Display classification results"""
    if st.session_state.df_result is not None:
        st.markdown("---")
        st.markdown("## 分类结果展示")

        with st.container(border=True):
            if st.session_state.is_multi_label:
                # Multi-label classification result display
                st.write("多标签分类结果：")
                # Get all category columns
                category_columns = [
                    col
                    for col in st.session_state.df_result.columns
                    if col.startswith("category_")
                ]

                # Create a new DataFrame containing only original text and category columns
                display_df = st.session_state.df_result[
                    [st.session_state.text_column] + category_columns
                ].copy()

                # Merge category columns into a list
                display_df["分类结果"] = display_df[category_columns].apply(
                    lambda row: [cat for cat, val in row.items() if val], axis=1
                )

                # Remove original category columns
                display_df = display_df.drop(columns=category_columns)

                st.dataframe(display_df)
            else:
                # Single-label classification result display
                st.write("单标签分类结果：")
                st.dataframe(st.session_state.df_result)

            # Provide download option
            csv = st.session_state.df_result.to_csv(
                index=False).encode("utf-8-sig")
            st.download_button(
                label="下载分类结果CSV",
                data=csv,
                file_name="classification_results.csv",
                mime="text/csv",
            )


def main():
    """Main function: control the entire application flow"""
    initialize_session_state()

    st.title("🔬 文本聚类分析")

    display_info_message()
    
    # Display project information
    display_project_info()
    
    st.markdown("---")
    
    display_workflow_introduction()

    handle_data_input_and_clustering()
    handle_custom_categories()
    review_clustering_results()
    display_classification_results()

    show_footer()


main()
