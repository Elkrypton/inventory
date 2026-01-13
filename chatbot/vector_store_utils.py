# chatbot/vector_store_utils.py
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
# Modern Import (v1.x)
from langchain_core.documents import Document

def add_to_vector_store(manufacturer):
    print("vector store triggered")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    index_path = "vector_store"

    try:
        vector_store = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
    except:
        vector_store = FAISS.from_documents([], embedding_model)  # Empty index if not exists

    # Format document
    content = f"""
    Product Name: {manufacturer.item}
    SKU: {manufacturer.sku}
    Date: {manufacturer.date_of_production}
    Location: {manufacturer.location}
    Quantity: {manufacturer.quantity}
    """
    document = Document(page_content=content.strip())

    # Add and save
    vector_store.add_documents([document])
    vector_store.save_local(index_path)
