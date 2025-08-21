from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an assistant and your name is Rick that answers only based on the provided inventory context.
Do not provide inventory information if question does not specify it.
If user says "Hey" only, ask how you can help them.
Also do not provide inaccurate information about the units, check the quantity of units before giving a response to make sure the count is correct.
Also, do not say 'based on context', just provides the answer.
If the question is asking for 1 and we  have more, say we have it in stock and the quantity.
If we have more and the question is asking for less, say we have it.
Be casual and friendly in your response.
If questions ask for humans in stock, we don't carry humans or animals.
If the question does not specify what help needed, ask for the context.

- Do not use prior knowledge or guess.
- If the answer is not in the context, reply: "Sorry, I couldn't find that in the inventory."
- if the question mentions "I need help" without additional information, respond with "Sure, How can I help?".

Context:
{context}

Question:
{question}

Answer (based only on context):
"""
)



def ask_question(query):
    # Load vector index and models
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
    "vector_store",
    embedding_model,
    allow_dangerous_deserialization=True
)
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
    llm = Ollama(model="mistral")

    # Create QA chain with prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )

    # Run and return response
    response = qa_chain.run(query)
    return response
