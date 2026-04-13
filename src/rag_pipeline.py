from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config import DOCS_DIR, CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def load_documents():
    """Charge tous les PDFs du dossier data/"""
    docs = []
    for pdf_path in Path(DOCS_DIR).glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        docs.extend(loader.load())
    print(f"{len(docs)} pages chargées")
    return docs

def split_documents(docs):
    """Découpe les documents en chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\nArticle", "\n\n", "\n", " "]
    )
    splits = splitter.split_documents(docs)
    print(f"{len(splits)} chunks créés")
    return splits

def build_vectorstore(splits):
    """Crée l'index ChromaDB"""
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=CHROMA_DIR
    )
    print(f"{vectorstore._collection.count()} chunks vectorisés")
    return vectorstore

def load_vectorstore():
    """Charge un index ChromaDB existant"""
    embedding = OpenAIEmbeddings()
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding
    )

def get_retriever(vectorstore, k=4):
    """Retourne le retriever"""
    return vectorstore.as_retriever(search_kwargs={"k": k})

def ask_rag(question: str, retriever) -> str:
    """Pose une question au pipeline RAG"""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Tu es un assistant juridique expert en droit du travail français.
Réponds en te basant UNIQUEMENT sur les extraits du Code du Travail fournis.
Cite les articles pertinents quand possible.
Réponds toujours en français.

Extraits du Code du Travail :
{context}"""),
        ("human", "{question}")
    ])
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"context": context, "question": question})

vectorstore_instance = load_vectorstore()

retriever_instance = get_retriever(vectorstore_instance)