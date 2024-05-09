import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama 
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain 
## loading documents

df = pd.read_csv("cards.csv")
loader = PyPDFLoader("meanings.pdf")
docs = loader.load()

## transformation by splitting
text_splitters = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap =200)
documents = text_splitters.split_documents(docs)


## embedding the documents as vector

db = FAISS.from_documents(documents,OllamaEmbeddings())

## initializing llm model
llm = Ollama(model="llama2")

## designing chat prompt template

prompt = ChatPromptTemplate.from_template("""
You are an experienced tarot reader. You derive meaningful interpretations
from the cards drawn and guide the querent with kindness, honesty and empathy . You 
refer to the symbolisms and mythology to empower the querent.
Cards_Drawn:{cards_drawn}
Question:{question}
"""
)

## initilalizing chain

document_chain = create_stuff_documents_chain(llm,prompt)

## initializing retriver

retriever= db.as_retriever()

## creating retrival chain 
retrieval_chain = create_retrieval_chain(retriever, document_chain)



def get_reading(card1,card2,card3,question):
    cards_drawn = df.at[card1, 'Name']+ ", " +df.at[card2, 'Name']+ ", " + df.at[card3, 'Name']
    response = retrieval_chain.invoke({"question": question, 
                                       "cards_drawn": cards_drawn })
    return response['answer']

if __name__ == "__main__":
    print(get_reading(0,0,0,"calling from backend"))