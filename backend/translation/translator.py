import os
import uuid
from typing import Dict, Any

from langfuse.langchain import CallbackHandler
from pydantic import BaseModel, Field

from langchain.chat_models import init_chat_model

from utils.llm_tools import LanguageModelChain


class TranslatedText(BaseModel):
    """Data model representing translated text."""

    translated_text: str = Field(..., description="Text content translated to Chinese")


SYSTEM_MESSAGE = """
你是一位精通多语言的翻译专家。你的任务是将给定的{text_topic}文本准确翻译成中文。请遵循以下指南：

1. 翻译要求：
   - 仔细阅读每条文本，理解其核心内容和语境。
   - 将文本准确翻译成中文，保持原意不变。
   - 确保翻译后的文本通顺、自然，符合中文表达习惯。
   - 如遇专业术语或特定概念，请尽可能找到恰当的中文对应表述。

2. 输出格式：
   - 对每条文本，输出对应的中文翻译。
   - 忽略原始文本中的特殊格式，按照一段话的形式输出翻译结果，不要包含特殊字符。

请确保翻译的准确性和一致性，不要遗漏任何内容。
"""

HUMAN_MESSAGE_TEMPLATE = """
请将以下{text_topic}文本翻译成中文。

```
{text_to_translate}
```

请按照系统消息中的指南进行翻译，并以指定的JSON格式输出结果，但不要在输出中重复json schema。
"""


def create_langfuse_handler(session_id: str, step: str) -> dict:
    """
    Create Langfuse callback configuration.

    Args:
        session_id (str): Session ID.
        step (str): Current step.

    Returns:
        dict: Configuration dictionary containing callback handler and metadata.
    """
    handler = CallbackHandler()
    metadata = {
        "langfuse_session_id": session_id,
        "langfuse_tags": ["translation"],
        "step": step,
    }
    return {"callbacks": [handler], "metadata": metadata}


class Translator:
    """Translator class for handling text translation tasks."""

    def __init__(self, temperature: float = 0.0):
        """
        Initialize the translator.

        Args:
            temperature (float): Temperature parameter for the language model, controls output randomness.
        """
        # init_chat_model supports multiple model providers
        # Reads model name from environment variable OPENAI_MODEL_NAME
        import os
        model_name = os.getenv("OPENAI_MODEL_NAME")
        self.language_model = init_chat_model(
            model=model_name,
            model_provider="openai",
            temperature=temperature,
        )
        self.translation_chain = LanguageModelChain(
            TranslatedText, SYSTEM_MESSAGE, HUMAN_MESSAGE_TEMPLATE, self.language_model
        )()

    async def translate(
        self, text: str, text_topic: str, session_id: str = None
    ) -> str:
        """
        Asynchronously translate a single text.

        Args:
            text (str): Text to be translated.
            text_topic (str): Text topic for context understanding.
            session_id (str, optional): Session ID for Langfuse monitoring.

        Returns:
            str: Translated text.

        Raises:
            ValueError: Raised when translation result format is incorrect.
            Exception: Raised when other errors occur during translation.
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        try:
            config = create_langfuse_handler(session_id, "translate")
            result = await self.translation_chain.ainvoke(
                {"text_to_translate": text, "text_topic": text_topic},
                config=config,
            )
            self._validate_translation_result(result)
            return result["translated_text"]
        except ValueError as ve:
            print(f"Translation result format is incorrect: {ve}")
            raise
        except Exception as e:
            print(f"Error occurred during translation: {e}")
            raise

    @staticmethod
    def _validate_translation_result(result: Dict[str, Any]) -> None:
        """
        Validate the format of translation result.

        Args:
            result (Dict[str, Any]): Translation result dictionary.

        Raises:
            ValueError: Raised when the result format is incorrect.
        """
        if not isinstance(result, dict) or "translated_text" not in result:
            raise ValueError("Translation result format is incorrect")
