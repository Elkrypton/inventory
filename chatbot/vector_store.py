# chatbot/build_vector_store.py
import os
import sys
import django
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# Django setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orders_report.settings")
django.setup()

from chatbot.export_inventory import export_inventory_data

# Prepare documents
texts = export_inventory_data()
documents = [Document(page_content=text) for text in texts]

# Build vector store
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_documents(documents, embedding_model)

# Save it
vector_store.save_local("vector_store")
print("✅ Vector store saved.")
