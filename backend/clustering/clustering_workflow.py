import os
import uuid
from typing import List, Dict, Any, Optional, Tuple

import pandas as pd
from langfuse.langchain import CallbackHandler
from langchain.chat_models import init_chat_model

from utils.llm_tools import LanguageModelChain
from utils.text_utils import (
    clean_text_columns,
    filter_invalid_text,
    dataframe_to_markdown_tables,
)
from backend.clustering.clustering_core import (
    Categories,
    ClassificationResult,
    INITIAL_CATEGORY_GENERATION_SYSTEM_MESSAGE,
    INITIAL_CATEGORY_GENERATION_HUMAN_MESSAGE,
    MERGE_CATEGORIES_SYSTEM_MESSAGE,
    MERGE_CATEGORIES_HUMAN_MESSAGE,
    SINGLE_LABEL_CLASSIFICATION_SYSTEM_MESSAGE,
    MULTI_LABEL_CLASSIFICATION_SYSTEM_MESSAGE,
    TEXT_CLASSIFICATION_HUMAN_MESSAGE,
)

# Initialize language model
# init_chat_model supports multiple model providers
# Reads model name from environment variable OPENAI_MODEL_NAME
# Reads configuration from environment variables OPENAI_API_KEY, OPENAI_BASE_URL
import os
model_name = os.getenv("OPENAI_MODEL_NAME")
language_model = init_chat_model(
    model=model_name,
    model_provider="openai",
    temperature=0.0,
)

def create_langfuse_handler(session_id: str, step: str) -> dict:
    """
    Create Langfuse callback configuration

    Args:
        session_id: Session ID
        step: Current step name

    Returns:
        dict: Configuration dictionary containing callback handler and metadata
    """
    handler = CallbackHandler()
    metadata = {
        "langfuse_session_id": session_id,
        "langfuse_tags": ["text_clustering"],
        "step": step,
    }
    return {"callbacks": [handler], "metadata": metadata}

def generate_unique_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate unique IDs for DataFrame in the format 'ID' followed by 6 digits

    Args:
        df: Input DataFrame

    Returns:
        pd.DataFrame: DataFrame with added unique ID column
    """
    df["unique_id"] = [f"ID{i:06d}" for i in range(1, len(df) + 1)]
    return df

def preprocess_data(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """
    Preprocess data: clean text column, filter invalid text, and generate unique IDs

    Args:
        df: Input DataFrame
        text_column: Name of the column containing text data

    Returns:
        pd.DataFrame: Preprocessed DataFrame
    """
    df = clean_text_columns(df)
    df = filter_invalid_text(df, text_column)
    df = generate_unique_ids(df)
    return df

def batch_texts(df: pd.DataFrame, text_column: str, batch_size: int = 100) -> List[str]:
    """
    Batch text data for processing

    Args:
        df: DataFrame containing text data
        text_column: Name of the text column
        batch_size: Number of texts per batch

    Returns:
        List[str]: List of batched texts
    """
    return [
        " ".join(df[text_column].iloc[i : i + batch_size].tolist())
        for i in range(0, len(df), batch_size)
    ]

def generate_initial_categories(
    texts: List[str],
    text_topic: str,
    category_count: int,
    session_id: str,
    additional_requirements: Optional[str] = None,
) -> List[Dict]:
    """
    Generate initial categories

    Args:
        texts: List of texts to be classified
        text_topic: Topic or background of the texts
        category_count: Expected number of categories to generate
        session_id: Session ID
        additional_requirements: Additional requirements (optional)

    Returns:
        List[Dict]: List of generated initial categories
    """
    config = create_langfuse_handler(session_id, "initial_categories")
    category_chain = LanguageModelChain(
        Categories,
        INITIAL_CATEGORY_GENERATION_SYSTEM_MESSAGE,
        INITIAL_CATEGORY_GENERATION_HUMAN_MESSAGE,
        language_model,
    )()

    categories_list = []
    for text_batch in texts:
        result = category_chain.invoke(
            {
                "text_topic": text_topic,
                "text_content": text_batch,
                "category_count": category_count,
                "additional_requirements": additional_requirements,
            },
            config=config,
        )
        categories_list.append(result)

    return categories_list

def merge_categories(
    categories_list: List[Dict],
    text_topic: str,
    min_categories: int,
    max_categories: int,
    session_id: str,
    additional_requirements: Optional[str] = None,
) -> Dict:
    """
    Merge generated categories

    Args:
        categories_list: List of initial categories
        text_topic: Topic or background of the texts
        min_categories: Minimum number of categories
        max_categories: Maximum number of categories
        session_id: Session ID
        additional_requirements: Additional requirements (optional)

    Returns:
        Dict: Dictionary of merged categories
    """
    config = create_langfuse_handler(session_id, "merge_categories")
    merge_chain = LanguageModelChain(
        Categories,
        MERGE_CATEGORIES_SYSTEM_MESSAGE,
        MERGE_CATEGORIES_HUMAN_MESSAGE,
        language_model,
    )()

    result = merge_chain.invoke(
        {
            "text_topic": text_topic,
            "classification_results": categories_list,
            "min_categories": min_categories,
            "max_categories": max_categories,
            "additional_requirements": additional_requirements,
        },
        config=config,
    )

    return result

def generate_categories(
    df: pd.DataFrame,
    text_column: str,
    text_topic: str,
    initial_category_count: int,
    min_categories: int,
    max_categories: int,
    batch_size: int = 100,
    session_id: Optional[str] = None,
    additional_requirements: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main function for generating categories

    Args:
        df: Input DataFrame
        text_column: Name of the text column
        text_topic: Topic or background of the texts
        initial_category_count: Initial number of categories
        min_categories: Minimum number of categories
        max_categories: Maximum number of categories
        batch_size: Batch size for processing
        session_id: Session ID (optional)
        additional_requirements: Additional requirements (optional)

    Returns:
        Dict[str, Any]: Dictionary containing generated categories, preprocessed DataFrame, and session ID
    """
    if session_id is None:
        session_id = str(uuid.uuid4())

    preprocessed_df = preprocess_data(df, text_column)
    batched_texts = batch_texts(preprocessed_df, text_column, batch_size)
    initial_categories = generate_initial_categories(
        batched_texts,
        text_topic,
        initial_category_count,
        session_id,
        additional_requirements,
    )
    merged_categories = merge_categories(
        initial_categories,
        text_topic,
        min_categories,
        max_categories,
        session_id,
        additional_requirements,
    )

    return {
        "categories": merged_categories,
        "preprocessed_df": preprocessed_df,
        "session_id": session_id,
    }

def classify_single_batch(
    text_batch: str,
    categories: Dict,
    text_topic: str,
    session_id: str,
    config: dict,
    classification_chain: LanguageModelChain,
    is_multi_label: bool,
) -> List[Dict]:
    """
    Classify a single batch of texts

    Args:
        text_batch: Text batch
        categories: Categories dictionary
        text_topic: Topic or background of the texts
        session_id: Session ID
        config: Langfuse configuration dictionary
        classification_chain: Classification chain
        is_multi_label: Whether it's multi-label classification

    Returns:
        List[Dict]: List of classification results
    """
    try:
        result = classification_chain.invoke(
            {
                "text_topic": text_topic,
                "categories": categories,
                "text_table": text_batch,
            },
            config=config,
        )
        return result["classifications"]
    except Exception as e:
        print(f"Error in batch classification for session {session_id}: {str(e)}")
        return []

def classify_texts(
    df: pd.DataFrame,
    text_column: str,
    id_column: str,
    categories: Dict,
    text_topic: str,
    session_id: str,
    classification_batch_size: int = 20,
    is_multi_label: bool = False,
) -> pd.DataFrame:
    """
    Classify texts

    Args:
        df: DataFrame containing text data
        text_column: Name of the text column
        id_column: Name of the ID column
        categories: Categories dictionary
        text_topic: Topic or background of the texts
        session_id: Session ID
        classification_batch_size: Batch size for classification
        is_multi_label: Whether it's multi-label classification

    Returns:
        pd.DataFrame: DataFrame containing classification results
    """
    config = create_langfuse_handler(session_id, "classify_texts")

    system_message = (
        MULTI_LABEL_CLASSIFICATION_SYSTEM_MESSAGE
        if is_multi_label
        else SINGLE_LABEL_CLASSIFICATION_SYSTEM_MESSAGE
    )

    classification_chain = LanguageModelChain(
        ClassificationResult,
        system_message,
        TEXT_CLASSIFICATION_HUMAN_MESSAGE,
        language_model,
    )()

    markdown_tables = dataframe_to_markdown_tables(
        df, [id_column, text_column], rows_per_table=classification_batch_size
    )

    classification_results = []
    for table in markdown_tables:
        try:
            result = classify_single_batch(
                table,
                categories,
                text_topic,
                session_id,
                config,
                classification_chain,
                is_multi_label,
            )
            classification_results.extend(result)
            # Save temporary file after processing each batch
            save_temp_results(classification_results, session_id, "text_classification")
        except Exception as e:
            print(f"Error processing batch in session {session_id}: {str(e)}")

    df_classifications = pd.DataFrame(classification_results)

    if is_multi_label:
        # Process multi-label classification results
        df_result = df.merge(
            df_classifications, left_on="unique_id", right_on="id", how="left"
        )
        df_result = df_result.drop(columns=["unique_id", "id"])
        # Expand categories column into multiple individual columns
        category_columns = df_result["categories"].apply(pd.Series)
        category_columns = category_columns.add_prefix("category_")
        df_result = pd.concat(
            [df_result.drop(columns=["categories"]), category_columns], axis=1
        )
    else:
        # Process single-label classification results
        df_result = df.merge(
            df_classifications, left_on="unique_id", right_on="id", how="left"
        )
        df_result = df_result.drop(columns=["unique_id", "id"])

    return df_result

def save_temp_results(results: List[Dict], task_id: str, entity_type: str):
    """
    Save temporary results to file.

    Args:
        results: List of classification results
        task_id: Task ID
        entity_type: Entity type
    """
    temp_dir = os.path.join("data", "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(
        temp_dir, f"classify_texts_{entity_type}_{task_id}.csv"
    )

    df = pd.DataFrame(results)
    df.to_csv(temp_file_path, index=False, encoding="utf-8-sig")