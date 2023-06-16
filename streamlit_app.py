import streamlit as st
from langchain import OpenAI

from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
OPENAI_API_KEY = 'nokey'
PINECONE_API_ENV = st.secrets["PINECONE_API_ENV"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "hinsdale-doings-try1" # put in the name of your pinecone index here
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
query = "Who was William Robbins? Please write 3 paragraphs explaining his impact on the development of Hinsdale"
# docs = docsearch.similarity_search(query)
# chain.run(input_documents=docs, question=query)




st.title('Hinsdale History Helper')

with st.sidebar:
   OPENAI_API_KEY = st.text_input('OpenAI API Key')

def generate_response(input_text):
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = docsearch.similarity_search(input_text)
    chain.run(input_documents=docs, question=input_text)   
  # llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  # st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Ask a Hinsdale hisotry question:', 'Who was William Robbins? Explain his impact on the development of Hinsdale')
  submitted = st.form_submit_button('Submit')
  if submitted:
    generate_response(text)
