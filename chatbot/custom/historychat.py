from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


from .vstore import getVectorStore
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, stream=True)


vectorstore = getVectorStore()
retriever = vectorstore.as_retriever()


### Contextualize question ###
contextualize_q_system_prompt = """Given a chat history and the latest user question about supplier\
which might reference docs in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)


### Answer question ###
qa_system_prompt = """You are an assistant for question-answering tasks about product suppliers, their products, services, online website so on. \
Refer to the following pieces of scraped data from their online websites to answer the question. \
If you don't make sense about question, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


### Statefully manage chat history ###
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def stream_runnable_fn(input_data):
    for word in input_data.split():
        yield {"output": word}

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)



from ..models import Message, ChatSession
import time

def answer(question, session_id):
    chat_session = ChatSession.objects.get(session_id=session_id)
    messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')
    message = Message.objects.create(chat_session=chat_session, role='assistant', content='')
    content = ''
    # stream_out = conversational_rag_chain.stream(
    #     {
    #         "input": question,
    #         # "chat_history": last_message,
    #     },
    #     config={"configurable": {"session_id": session_id}},
    # )
    # for chunk in stream_out:
    #     try:
    #         if 'answer' in chunk:
    #             print(chunk['answer'], end='')
    #             content += chunk['answer']
    #             yield chunk['answer']
    #     except Exception as err:
    #         print(str(err), "error")
    for i in range(10):
        content += 'what is that '
        time.sleep(0.5)
        yield 'what is that '
    message.content = content
    print('message is ', message)
    message.save()