from abc import ABC, abstractmethod

from langchain_openai import ChatOpenAI

from app.core.settings import Settings


class LLMBaseAdapter(ABC):
    @staticmethod
    @abstractmethod
    def get_model(settings: Settings): ...


class ChatGpt(LLMBaseAdapter):
    @staticmethod
    def get_model(settings: Settings):
        return ChatOpenAI(
            model_name=settings.CHAT_GPT_MODEL_NAME,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.CHAT_GPT_API_BASE,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )
