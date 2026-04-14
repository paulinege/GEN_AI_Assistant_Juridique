"""
Script pour initialiser l'index ChromaDB
Exécutez-le une seule fois pour créer l'index
"""

from src.rag_pipeline import load_documents, split_documents, build_vectorstore

if __name__ == "__main__":
    print("Chargement des documents...")
    docs = load_documents()
    
    print("Division des documents...")
    splits = split_documents(docs)
    
    print("Construction de l'index...")
    vectorstore = build_vectorstore(splits)
    
    print("✅ Index ChromaDB créé avec succès !")