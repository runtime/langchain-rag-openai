# Aruino Sensor RAG w/OpenAI Embedding & Mistral (on Ollama) for Query Match

This is an MVP of a LLM Document Search RAG. 

Requirements Doc:
* Scan PDF (pypdf) (AWS Textract)
* Create pages
* Chunk pages (langchain) 
* Embeddings (openAI) 
* Store in Vector DB (Chroma) 
* Test our embeddings (pyTest)
* Retrieve with search query (nistral)

## Use Guide
### Install dependencies
run this command to install dependencies in the `requirements.txt` file. 

```python
pip install -r requirements.txt
```




## Installs
```python
pip install pytest 
pip install pyPdf
```

## Step 1: Start or Add to Existing Chroma db

To Scan all the pdf files in the data folder and put them into the RAG run:

```python
python load_pdf.py
```
This will scan the pdfs using pypdf through langchain document loader, split the docs into pages and then will chunk it. Chunks are embedded and stored in Chroma
## Step 2: Query the database

Query the Chroma DB and use Mistral to create an answer

```python
python query_data.py "Your question relevant to the context of the application"
```

## Step 3: Test the Query Returns using PyTest and Mistral

Test Mistral's answers using PyTest 

```python
pytest test_cases.py
```


Thanks to pixegami tutorial for pyTest and langchain chunking
