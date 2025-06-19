from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

def build_knowledge_base(text_file_path):
    """
    Build a FAISS-based vector database from the provided text file.
    Args:
        text_file_path (str): Path to a .txt file.
    Returns:
        FAISS: A vectorstore of embedded document chunks.
    """
    loader = TextLoader(text_file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(texts, embeddings)

    return db

def retrieve_relevant_context(db, query, k=3):
    """
    Retrieve top-k similar chunks from the vector DB for a given query.
    Args:
        db (FAISS): The FAISS vectorstore.
        query (str): The question/query.
        k (int): Number of top results to retrieve.
    Returns:
        List[Document]: List of most relevant document chunks.
    """
    return db.similarity_search(query, k=k)