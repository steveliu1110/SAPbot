from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI


from dotenv import load_dotenv
import os

load_dotenv()

# Define summarization prompt
summarize_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    The content is scraped data from Supplier website.
    Summarize the content with less than 1024 token by focusing on their websites url(like https://example.com), products, capabilities/services, certifications(like ISO XXXX), locations, and recent products with date if possible(like 5G watch in April)
    And only rely on real information.
    \n\n{text}\n\nSummarized content:
    """
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
