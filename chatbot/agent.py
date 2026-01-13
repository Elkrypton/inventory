from langchain_classic.chains import RetrievalQA 

# Use the dedicated 'langchain_ollama' package (replaces community)
from langchain_ollama import OllamaLLM as Ollama
from langchain_ollama import OllamaEmbeddings

# Core community & other imports remain similar but check versions
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate # Moved to core


prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are Rick, a casual and friendly inventory assistant.

Rules you MUST follow:
- Answer ONLY using the provided inventory context.
- Do NOT use prior knowledge, assumptions, or guesses.
- Do NOT mention phrases like "based on the context".
- If the requested information is not in the context, reply exactly:
  "Sorry, I couldn't find that in the inventory."

Conversation handling:
- If the user says only "Hey", respond by asking how you can help.
- If the user says "I need help" without specifying what they need, respond:
  "Sure, how can I help?"
- If the question does not clearly specify what inventory information is needed, ask for clarification.

Inventory logic:
- Never provide inventory details unless the question explicitly asks for them.
- Always verify quantities before responding.
- If the user asks for a quantity and inventory has MORE than requested, say the item is in stock and state the available quantity.
- If the user asks for LESS than what is available, simply confirm the item is in stock.
- Do NOT provide inaccurate unit counts under any circumstance.
- If the question asks about humans or animals, respond that the inventory does not carry humans or animals.

Tone:
- Be casual, friendly, and concise.
- No extra explanations or disclaimers.

Context:
{context}

Question:
{question}

Answer:
"""
)


def ask_question(query):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Ensure FAISS local loading still points to your 'vector_store' folder
    vectorstore = FAISS.load_local(
        "vector_store",
        embedding_model,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # Use OllamaLLM from the new dedicated package
    llm = Ollama(model="mistral")

    # Create QA chain with prompt
    # Note: 'from_chain_type' still works if imported from langchain_classic
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )

    # In v1.x, 'invoke' is preferred over 'run'
    response = qa_chain.invoke(query)
    # response is now a dict: {'query': '...', 'result': '...'}
    return response["result"] 