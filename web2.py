import streamlit as st
import random
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
#from langchain_openai import ChatOpenAI
#from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama 
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain 
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import StrOutputParser
## loading documents

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

df = pd.read_csv("cards.csv")
loader = PyPDFLoader("meanings.pdf")
docs = loader.load()

## transformation by splitting
text_splitters = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap =200)
documents = text_splitters.split_documents(docs)


## embedding the documents as vector

db = FAISS.from_documents(documents,OpenAIEmbeddings())


## designing chat prompt template

prompt = ChatPromptTemplate.from_template(""" Draw 3 cards only. Name of cards are provided in context.
You are an experienced tarot reader. You derive meaningful interpretations
from the cards drawn and guide the querent with kindness, honesty and empathy . You 
refer to the symbolisms and mythology to empower the querent.

Question:{input}
"""
)

llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser() 
chain = prompt | llm | output_parser

## initilalizing chain


st.title("Tarot reader")

question = st.text_input("Ask your question.")
card1 = random.randint(0, 77)
card2 = random.randint(0, 77)
while card1 == card2:
    card2 =  random.randint(0, 77)
card3 = random.randint(0, 77)
while (card3 == card2 or  card1==card3):
    card2 =  random.randint(0, 77)

if question:
    
   

    image_paths = [f"images/{card1}.png",f"images/{card2}.png",f"images/{card3}.png"]
    st.image(image_paths, width=200)

    cards_drawn = df.at[card1, 'Name']+ ", " +df.at[card2, 'Name']+ ", " + df.at[card3, 'Name']
    st.write(cards_drawn)
    query = cards_drawn + " " + question
    result = chain.invoke({'input': query})
    st.write(result)