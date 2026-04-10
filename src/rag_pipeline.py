"""
Partie 1 — Pipeline RAG
Chargement, découpage, vectorisation et retrieval des PDFs du Code du Travail
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

DOCS_DIR = Path(os.getenv("DOCS_DIR", "./data"))
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")


def load_documents():
    """Charge tous les PDFs du dossier data/"""
    docs = []
    pdf_files = list(DOCS_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"Aucun PDF trouvé dans {DOCS_DIR}")
    for pdf_path in pdf_files:
        print(f"Chargement : {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        docs.extend(loader.load())
    print(f"→ {len(docs)} pages chargées")
    return docs


def split_documents(docs):
    """Découpe les documents en chunks adaptés aux textes juridiques"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\nArticle", "\n\n", "\n", " "]
    )
    splits = splitter.split_documents(docs)
    print(f"→ {len(splits)} chunks créés")
    return splits


def build_vectorstore(splits):
    """Crée ou charge l'index ChromaDB"""
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=CHROMA_DIR
    )
    print(f"→ Index ChromaDB sauvegardé dans {CHROMA_DIR}")
    return vectorstore


def load_vectorstore():
    """Charge un index ChromaDB existant"""
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding
    )
    return vectorstore


def get_retriever(vectorstore, k=4):
    """Retourne un retriever configuré"""
    return vectorstore.as_retriever(search_kwargs={"k": k})


if __name__ == "__main__":
    docs = load_documents()
    splits = split_documents(docs)
    vectorstore = build_vectorstore(splits)
    retriever = get_retriever(vectorstore)

    # Test rapide
    query = "Quel est le délai de préavis pour un CDI ?"
    results = retriever.invoke(query)
    print(f"\nQuestion : {query}")
    print(f"→ {len(results)} chunks récupérés")
    print(f"\nExtrait : {results[0].page_content[:300]}...")
