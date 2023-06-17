import streamlit as st
from langchain import OpenAI

from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
import pinecone
OPENAI_API_KEY = 'nokey'
PINECONE_API_ENV = st.secrets["PINECONE_API_ENV"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "hinsdale-history-try2" # put in the name of your pinecone index here
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
query = "Who was William Robbins? Please write 3 paragraphs explaining his impact on the development of Hinsdale"
# docs = docsearch.similarity_search(query)
# chain.run(input_documents=docs, question=query)




st.title('Hinsdale History Helper')

with st.sidebar:
   OPENAI_API_KEY = st.text_input('OpenAI API Key')

def generate_response(input_text):
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name = 'gpt-3.5-turbo')
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    docs = docsearch.similarity_search(input_text, k=10)
    chain = load_qa_chain(llm, chain_type="stuff")
    st.info(chain.run(input_documents=docs, question=input_text))
    # chain = load_summarize_chain(llm, chain_type="map_reduce")
    # st.info(chain.run(docs))
    for i, d in enumerate(docs):
        st.info(f"\n## Document {i}\n")
        st.info(d.page_content)


with st.form('my_form'):
  text = st.text_area('Ask a Hinsdale history question:', 'Who was William Robbins? Explain his impact on the development of Hinsdale')
  submitted = st.form_submit_button('Submit')
  if submitted:
    generate_response(text)
