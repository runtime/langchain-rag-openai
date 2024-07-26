#load arg generator for flagging db
import argparse
#from from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
#splitter lib
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
#global utils function for embeddings
from get_embedding_function import get_embedding_function
#chroma
from langchain_community.vectorstores import Chroma
import os
#DB persistence
import shutil




CHROMA_PATH = "chroma_db"
FILE_PATH = "data"


def main():
    print("f[main]")
    init()

def init():
    print("f[init] ✨")

    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    # load_pdf(file_path) <-- uses pdfloaders splitter
    documents = load_documents() #<-- uses langchain splitter
    #documents returns both the content and the meta data
    print("f[init] documents[0]: ", documents[0])
    print("f[init] documents[0]: ", documents[1])
    #use split_docs function which uses langchain recursive split
    chunks = split_documents(documents)
    #print("f[init] chunks[0]:  ", chunks[0])
    add_to_chroma(chunks)



# def load_pdf(FILE_PATH: str) -> list[str]:
#     loader = PyPDFLoader(FILE_PATH)
#     #load_and_split seems the same
#     pages = loader.load_and_split()
#     print("f[load_pdf] complete, pages: ", len(pages))
#     print("f[load_pdf] (example) page 1: ", pages[0].page_content)
#     return pages

def load_documents():
    print("f[load_documents] FILE_PATH ", FILE_PATH)
    #PyPDFLoader does one file
    #loader = PyPDFLoader(FILE_PATH)
    loader = PyPDFDirectoryLoader(FILE_PATH) #<-- Directory loader is needed for recursive file loading
    return loader.load()

#recursive text splitter
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

# multi use for storing and retrieving
# def get_embeddings():
#     embeddings = get_embedding_function()
#     return embeddings

#creates a new database
# def add_to_chroma(chunks):
#     if os.path.exists(CHROMA_PATH):
#         print('[load_pdf] chroma db already exists')
#         shutil.rmtree(CHROMA_PATH)
#     vectordb = Chroma.from_documents(documents=chunks, embedding=get_embeddings(), persist_directory=CHROMA_PATH)
#     print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

#add to existing chroma db. credit to pixegami for the chunking with ids to solve the page vs chunk id issue
def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default?"
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
            print("new_chunks: ", new_chunks)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)



if __name__ == "__main__":
    main()