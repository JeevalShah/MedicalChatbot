from langchain_huggingface import HuggingFaceEmbeddings
from flask import Flask, render_template, jsonify, request
from langchain.vectorstores import Pinecone as PC
import pinecone
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
#from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os


PROMPT_TEMPLATE="""
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""


#download embedding model
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
INDEX_NAME = os.environ['INDEX_NAME']


embeddings = download_hugging_face_embeddings()

docsearch=PC.from_existing_index(INDEX_NAME, embeddings)

PROMPT=PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}

llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8}
                          )

qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)



@app.route("/")
def index():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 3000, debug= True)