from .export_inventory import export_inventory_data
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
faiss_index = FAISS.load_local(
    "vector_store",
    embedding_model,
    allow_dangerous_deserialization=True
)

# Load local LLM instead of HuggingFaceHub (no token needed)
model_name = "google/flan-t5-small"  # You can upgrade to 'flan-t5-base' if you have more RAM/VRAM

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

hf_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
local_llm = HuggingFacePipeline(pipeline=hf_pipeline)

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(llm=local_llm, retriever=faiss_index.as_retriever())

def get_chatbot_response(user_input):
    return qa_chain.run(user_input)
