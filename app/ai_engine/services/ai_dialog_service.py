from typing import List

from injector import Inject
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.utils import Output
from langchain_core.vectorstores import VectorStoreRetriever

from app.ai_engine.llm_adapters import ChatGpt
from app.ai_engine.ports import AIDialogPort
from app.core.settings import Settings


class AIDialogService(AIDialogPort):
    def __init__(
        self,
        settings: Inject[Settings],
    ):
        self.llm = ChatGpt.get_model(settings=settings)

    @staticmethod
    def format_docs(docs: List) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    @property
    def prompt(self):
        return PromptTemplate(
            template="""
            Context:
            {context}

            Question:
            {question}

            Answer concisely and relevantly, providing only the most pertinent information from the given context.
            If the context is insufficient, indicate this and suggest that the user ask a more specific question.

            Constraints:
            - The data may be fragmented. If necessary, include context to maintain answer coherence.

            Format:
            - Ensure the answer is clear, structured, and easy to understand.
            - If additional information may be useful, suggest specific areas for further questions.
            """,
            input_variables=[
                "context",
                "question",
            ],
        )

    def get_answer(self, retriever_db: VectorStoreRetriever, question: str) -> Output:
        rag_chain = (
            {
                "context": retriever_db | self.format_docs,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
            # | StrOutputParser()
        )
        return rag_chain.invoke(question)
