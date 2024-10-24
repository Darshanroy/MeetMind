from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

class PromptFraming:
    def __init__(self, llm, vector_store):
        """
        Initialize the PromptFraming class with the LLM and vector store.
        """
        self.llm = llm
        self.vector_store = vector_store

        # Define the contextualization prompt for reformulating questions based on chat history
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """Given a chat history and the latest user question 
                which might reference context in the chat history, formulate a standalone question 
                which can be understood without the chat history. Do NOT answer the question, 
                just reformulate it if needed and otherwise return it as is."""),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # Define the chat prompt template for QA
        self.qa_prompt_template = ChatPromptTemplate.from_template("""
            Answer the following question based only on the provided context. 
            Think step by step before providing a detailed answer. 
            I will tip you $1000 if the user finds the answer helpful.
            <context>
            {context}
            </context>
            Question: {input}
        """)

        # Create the question answer chain
        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.qa_prompt_template)

        # Create the history-aware retriever
        self.history_aware_retriever = create_history_aware_retriever(
            self.llm, self.vector_store.as_retriever(), self.contextualize_q_prompt
        )

        # Create the retrieval chain
        self.retrieval_chain = create_retrieval_chain(self.history_aware_retriever, self.question_answer_chain)

        # Manage chat history
        self.chat_history_store = {}

    def get_chat_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Fetches the chat history for the given session.
        """
        if session_id not in self.chat_history_store:
            self.chat_history_store[session_id] = ChatMessageHistory()
        return self.chat_history_store[session_id]

    def create_conversational_rag_chain(self):
        """
        Create the conversational RAG chain with chat history management.
        """
        conversational_rag_chain = RunnableWithMessageHistory(
            self.retrieval_chain,
            self.get_chat_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
        return conversational_rag_chain
