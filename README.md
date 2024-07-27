# Langchain RAG w/OpenAI 

Requirements: 
* Scan PDF (pypdf) (AWS Textract)
* Create pages
* Chunk pages (langchain) 
* Embeddings (openAI) 
* Store in Vector DB (Chroma) 
* Test our embeddings (pyTest)
* Retrieve with search query (nistral)

## Install dependencies
run this command to install dependencies in the `requirements.txt` file. 

```python
pip install -r requirements.txt
```

### Parse a PDF
This project uses Langchain document_loaders to parse the PDF
https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/pdf/

```python
pip install pyPDF

### Create local Chroma database

Create a local Chroma DB. You can save it and upload to OpenAI or other vector store.

```python
python load_pdf.py
```

## Query the database

Query the Chroma DB.

```python
python query_data.py "Your question relevant to the context of the application"
```

> Project assumes a .env file. Use EnvFile plugin for PyCharm if using an IDE

based on pixegami tutorial on langchain
