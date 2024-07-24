#openai
from langchain_openai import OpenAIEmbeddings
import openai
#env
from dotenv import load_dotenv
import os


load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

def get_embedding_function():
    embeddings = OpenAIEmbeddings()
    return embeddings