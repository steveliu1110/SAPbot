import chromadb
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings 
from dotenv import load_dotenv
import os

load_dotenv()

def getVectorStore():
	storage_path = os.getenv('CHROMA_STORAGE_PATH')
	print(storage_path)
	if storage_path is None:
		raise ValueError('STORAGE_PATH environment variable is not set')
	
	embed_model = os.getenv('OLLAMA_EMBEDDING_MODEL')
	
	persistent_client = chromadb.PersistentClient(storage_path)
	collection = persistent_client.get_or_create_collection(name="SAP")
	vector_store_from_client = Chroma(
		client=persistent_client,
		collection_name="SAP",
		embedding_function=OllamaEmbeddings(model = embed_model),
	)
	return vector_store_from_client


def updateChroma(docs, ids):
	vstore = getVectorStore()
	vstore.add_documents(documents=docs, ids=ids)

