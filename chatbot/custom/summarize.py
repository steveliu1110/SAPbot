from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI


from dotenv import load_dotenv
import os

load_dotenv()

# Define summarization prompt
summarize_prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following content:\n\n{text}\n\nSummarized content:"
)

# Summarization chain
summarize_chain = LLMChain(
    llm=ChatOpenAI(
        openai_api_key = os.getenv('OPENAI_API_KEY'),
        model="gpt-4o"),
    prompt=summarize_prompt
)

# Summarize long documents
def compress_documents(documents):
    summaries = [summarize_chain.run({"text": doc}) for doc in documents]
    print(summaries)
    return summaries


if __name__ == "__main__":
    with open('sss', 'r') as file:
        content = ['Personalization: Integrating user profiles and historical interactions to personalize responses, making RAG models more effective in customer service and recommendation systems.'
        'Knowledge Grounding: Using external knowledge bases not just for retrieval but also for grounding the responses in verifiable facts, which is crucial for educational and informational applications.'
        'Efficient Indexing: Employing more efficient data structures and algorithms for indexing the database to speed up retrieval and reduce computational costs.']
        print(content)
        compress_documents(content)