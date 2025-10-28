from typing import Any, Type

from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class LanguageModelChain:
    """Language model chain for processing input and generating structured output."""

    def __init__(
        self, model_cls: Type[BaseModel], sys_msg: str, user_msg: str, model: Any
    ):
        """
        Initialize LanguageModelChain instance.

        Args:
            model_cls: Pydantic model class that defines the output structure.
            sys_msg: System message.
            user_msg: User message.
            model: Language model instance.
        """
        if not issubclass(model_cls, BaseModel):
            raise ValueError("model_cls must be a subclass of Pydantic BaseModel")
        if not isinstance(sys_msg, str) or not isinstance(user_msg, str):
            raise ValueError("sys_msg and user_msg must be strings")
        if not hasattr(model, "invoke"):
            raise ValueError("model must be a LangChain Runnable object (must have invoke method)")

        self.model_cls = model_cls
        self.parser = JsonOutputParser(pydantic_object=model_cls)

        format_instructions = """
Output your answer as a JSON object that conforms to the following schema:
```json
{schema}
```

Important instructions:
1. Ensure your JSON is valid and properly formatted.
2. Do not include the schema definition in your answer.
3. Only output the data instance that matches the schema.
4. Do not include any explanations or comments within the JSON output.
        """

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", sys_msg + format_instructions),
                ("human", user_msg),
            ]
        ).partial(schema=model_cls.model_json_schema())

        self.chain = self.prompt_template | model | self.parser

    def __call__(self) -> Any:
        """Invoke the processing chain."""
        return self.chain
