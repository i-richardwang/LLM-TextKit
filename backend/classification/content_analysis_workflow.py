import uuid
import asyncio
from typing import List

from langchain.chat_models import init_chat_model

from utils.llm_tools import LanguageModelChain
from backend.classification.content_analysis_core import (
    ContentAnalysisResult,
    ContentAnalysisInput,
    CONTENT_ANALYSIS_SYSTEM_PROMPT,
    CONTENT_ANALYSIS_HUMAN_PROMPT,
)
from langfuse.langchain import CallbackHandler


class TextContentAnalysisWorkflow:
    """Workflow class for text content analysis"""

    def __init__(self):
        """Initialize the text content analysis workflow"""
        # init_chat_model supports multiple model providers
        # Reads model name from environment variable OPENAI_MODEL_NAME
        import os
        model_name = os.getenv("OPENAI_MODEL_NAME")
        self.language_model = init_chat_model(
            model=model_name,
            model_provider="openai",
            temperature=0.0,
        )
        self.analysis_chain = LanguageModelChain(
            ContentAnalysisResult,
            CONTENT_ANALYSIS_SYSTEM_PROMPT,
            CONTENT_ANALYSIS_HUMAN_PROMPT,
            self.language_model,
        )()

    def analyze_text(
        self, input_data: ContentAnalysisInput, session_id: str = None
    ) -> ContentAnalysisResult:
        """
        Execute a single text content analysis task

        Args:
            input_data: Input data containing the text to be analyzed and its context
            session_id: Optional session ID

        Returns:
            Analysis result containing validity, sentiment, and sensitive information flag
        """
        session_id = session_id or str(uuid.uuid4())
        config = create_langfuse_handler(session_id, "content_analysis")

        result = self.analysis_chain.invoke(
            {
                "text": input_data.text,
                "context": input_data.context,
            },
            config=config,
        )
        return ContentAnalysisResult(**result)

    def batch_analyze(
        self, texts: List[str], context: str, session_id: str
    ) -> List[ContentAnalysisResult]:
        """
        Execute batch text content analysis tasks

        Args:
            texts: List of texts to be analyzed
            context: Context or topic of the texts
            session_id: Session ID for the batch task

        Returns:
            List of analysis results
        """
        return [
            self.analyze_text(
                ContentAnalysisInput(text=text, context=context), session_id
            )
            for text in texts
        ]

    async def async_analyze_text(
        self, input_data: ContentAnalysisInput, session_id: str = None
    ) -> ContentAnalysisResult:
        """
        Asynchronously execute a single text content analysis task

        Args:
            input_data: Input data containing the text to be analyzed and its context
            session_id: Optional session ID

        Returns:
            Analysis result containing validity, sentiment, and sensitive information flag
        """
        session_id = session_id or str(uuid.uuid4())
        config = create_langfuse_handler(session_id, "content_analysis")

        result = await self.analysis_chain.ainvoke(
            {
                "text": input_data.text,
                "context": input_data.context,
            },
            config=config,
        )
        return ContentAnalysisResult(**result)

    async def async_batch_analyze(
        self, texts: List[str], context: str, session_id: str, max_concurrency: int = 3
    ) -> List[ContentAnalysisResult]:
        """
        Asynchronously execute batch text content analysis tasks

        Args:
            texts: List of texts to be analyzed
            context: Context or topic of the texts
            session_id: Session ID for the batch task
            max_concurrency: Maximum concurrency level

        Returns:
            List of analysis results
        """
        semaphore = asyncio.Semaphore(max_concurrency)

        async def analyze_with_semaphore(text):
            async with semaphore:
                input_data = ContentAnalysisInput(text=text, context=context)
                return await self.async_analyze_text(input_data, session_id)

        tasks = [analyze_with_semaphore(text) for text in texts]
        return await asyncio.gather(*tasks)


def create_langfuse_handler(session_id: str, step: str) -> dict:
    """
    Create Langfuse callback configuration

    Args:
        session_id: Session ID
        step: Processing step

    Returns:
        Configuration dictionary containing callback handler and metadata
    """
    handler = CallbackHandler()
    metadata = {
        "langfuse_session_id": session_id,
        "langfuse_tags": ["content_analysis"],
        "step": step,
    }
    return {"callbacks": [handler], "metadata": metadata}
