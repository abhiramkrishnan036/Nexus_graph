import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq  # New Import
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer

# 1. Load secrets
load_dotenv()

# 2. Initialize Groq as the 'Brain'
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
graph = Neo4jGraph()

def process_pdf(file_path):
    print(f"--- Starting Ingestion for: {file_path} ---")
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    
    # AI Extraction logic
    llm_transformer = LLMGraphTransformer(llm=llm)
    print("Groq AI is now extracting entities and relationships...")
    graph_documents = llm_transformer.convert_to_graph_documents(pages)
    
    # Save to Neo4j
    graph.add_graph_documents(graph_documents)
    print("--- Knowledge Graph Successfully Updated! ---")

if __name__ == "__main__":
    process_pdf("backend/uploads/GraphRAG_Project_Blueprint.pdf")
    