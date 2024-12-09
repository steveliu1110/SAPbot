contextualize_q_system_prompt = """
Given a chat history and the latest user question about SAP suppliers\
which might reference docs in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is.
"""

print(contextualize_q_system_prompt)