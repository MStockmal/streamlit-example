pip install langchain --upgrade
pip3 install pinecone-client

from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
OPENAI_API_KEY = "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"
PINECONE_API_KEY = '2f8ad2cb-9fc5-41b3-bd63-b568bd67a013'
PINECONE_API_ENV = 'us-west4-gcp-free'
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "hinsdale-doings-try1" # put in the name of your pinecone index here
docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
chain = load_qa_chain(llm, chain_type="refine")
query = "Who was William Robbins? Please write 3 paragraphs explaining his impact on the development of Hinsdale"
docs = docsearch.similarity_search(query)
# chain.run(input_documents=docs, question=query)


import streamlit as st
from langchain import OpenAI

st.title('🦜🔗 Langchain Quickstart App')

with st.sidebar:
  openai_api_key = st.text_input('OpenAI API Key')

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are 3 key advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if submitted:
    generate_response(text)
