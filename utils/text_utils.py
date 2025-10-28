from typing import List, Literal, Union
import pandas as pd
import regex as re


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean all string columns in DataFrame by replacing specific punctuation with backticks
    and handling consecutive characters (removing consecutive underscores and spaces, keeping only one).

    Args:
        df (pd.DataFrame): DataFrame containing text columns to be cleaned

    Returns:
        pd.DataFrame: Copy of DataFrame with cleaned text columns

    Raises:
        ValueError: If input is not a pandas DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    def _clean_text(text: Union[str, float]) -> str:
        if pd.isna(text):
            return ""
        text = str(text)
        text = re.sub(r"['''\"" "{}]", "`", text)
        text = re.sub(r"_{2,}", "_", text)
        text = re.sub(r"\s{2,}", " ", text)
        return text

    cleaned_df = df.copy()
    for col in cleaned_df.select_dtypes(include=["object"]):
        cleaned_df[col] = cleaned_df[col].apply(_clean_text)

    return cleaned_df


def filter_invalid_text(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    """
    Filter rows with invalid text in the specified column from the dataset.

    Args:
        df (pd.DataFrame): Input dataset
        text_col (str): Name of the text column to check

    Returns:
        pd.DataFrame: Filtered dataset

    Raises:
        ValueError: If input is not a pandas DataFrame or the specified column doesn't exist
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    if text_col not in df.columns:
        raise ValueError(f"Specified column '{text_col}' does not exist in DataFrame")

    def is_valid_text(text):
        if pd.isna(text):
            return False
        text = str(text).strip()
        if (
            not text
            or re.match(r"^[\s\p{P}]+$", text, re.UNICODE)
            or text.isdigit()
            or len(set(text)) == 1
            or re.match(r"^(.)\1*(?:(.)\2*){0,2}$", text)
            or not re.search(r"[\p{L}\p{N}]", text, re.UNICODE)
        ):
            return False
        return True

    return df[df[text_col].apply(is_valid_text)]


def dataframe_to_markdown_tables(
    df: pd.DataFrame,
    cols: List[str],
    rows_per_table: int = 20,
    nan_drop_method: Literal["any", "all"] = "any",
    output_format: Literal["list", "dataframe"] = "list",
) -> Union[List[str], pd.DataFrame]:
    """
    Convert input DataFrame into batched Markdown tables.

    Args:
        df (pd.DataFrame): Input DataFrame
        cols (List[str]): Columns to include in Markdown tables
        rows_per_table (int, optional): Number of rows per Markdown table. Defaults to 20.
        nan_drop_method (Literal["any", "all"], optional): Method to drop rows with NaN values. Defaults to "any".
        output_format (Literal["list", "dataframe"], optional): Output format. Defaults to "list".

    Returns:
        Union[List[str], pd.DataFrame]: List of Markdown tables or DataFrame containing Markdown tables

    Raises:
        ValueError: If input parameters are invalid
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
    if not isinstance(cols, list) or not all(col in df.columns for col in cols):
        raise ValueError("cols must be a valid list of column names")
    if not isinstance(rows_per_table, int) or rows_per_table <= 0:
        raise ValueError("rows_per_table must be a positive integer")
    if nan_drop_method not in ["any", "all"]:
        raise ValueError("nan_drop_method must be 'any' or 'all'")
    if output_format not in ["list", "dataframe"]:
        raise ValueError("output_format must be 'list' or 'dataframe'")

    cleaned_df = df.dropna(subset=cols, how=nan_drop_method)
    text_cols = [col for col in cols if cleaned_df[col].dtype == "object"]
    for col in text_cols:
        cleaned_df[col] = cleaned_df[col].str.replace("\r\n|\n", " ", regex=True)

    table_data = cleaned_df[cols]
    markdown_tables = []

    for start_index in range(0, len(table_data), rows_per_table):
        table_subset = table_data.iloc[start_index : start_index + rows_per_table]
        table_header = "| " + " | ".join(cols) + " |\n"
        table_separator = "| " + " | ".join(["---"] * len(cols)) + " |\n"
        table_rows = "".join(
            f"| {' | '.join(map(str, row))} |\n" for _, row in table_subset.iterrows()
        )
        markdown_tables.append(table_header + table_separator + table_rows)

    return (
        markdown_tables
        if output_format == "list"
        else pd.DataFrame(markdown_tables, columns=["Markdown Table"])
    )
