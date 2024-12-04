import openai
from .summarize import compress_documents
from dotenv import load_dotenv  
import os 

def answer_user_prompt(question, vectorstore):  
	load_dotenv()
	retriever = vectorstore.as_retriever(
		search_type="similarity",
		search_kwargs={"k": 3},
	)
	relevant_docs = retriever.invoke(question)
	summary = compress_documents(relevant_docs)
	print(summary)
	
	openai.api_key = os.getenv('OPENAI_API_KEY')  
	print(openai.api_key)
	system_message = """You are a friendly assistant. Your job is to answer the user's question based on the documentation provided below."""  
	
	user_message = f"Docs:\n\n{summary}\n\nQuestion: {question}"  

	# Ensure correct call to OpenAI API  
	response = openai.chat.completions.create(  
		model="gpt-3.5-turbo",  
		messages=[  
			{"role": "system", "content": system_message},  
			{"role": "user", "content": user_message}  
		],
		stream=True
	)  

	print(response,'wwerwerwe')
	for part in response:
		# The OpenAI API streams the response in parts
		print(part)
		yield part.choices[0].delta.content
	# if response and response.choices:  
	# 	response_content = response.choices[0].message.content.strip()  
	# 	return response_content
	# else:  
	# 	raise ValueError("The OpenAI API response did not contain response data.")  
	# return
	