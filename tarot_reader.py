import streamlit as st
import random
import pandas as pd
import openai


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

import toml



# Load environment variables
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to draw tarot cards
def draw_cards():
    df = pd.read_csv("cards.csv")
    card1 = random.randint(0, 77)
    card2 = random.randint(0, 77)
    while card1 == card2:
        card2 = random.randint(0, 77)
    card3 = random.randint(0, 77)
    while (card3 == card2 or  card1 == card3):
        card3 = random.randint(0, 77)

    cards_drawn = df.at[card1, 'Name'] + ", " + df.at[card2, 'Name'] + ", " + df.at[card3, 'Name']
    image_path = [f"images/{card1}.png",
                  
                  f"images/{card2}.png",
                  
                  f"images/{card3}.png",
                  ]
    
    return cards_drawn , image_path

if __name__ == "__main__":
    # Initialize chat history
    chat_history = []
    
    # Initialize Streamlit app
    st.title("Myra, Tarot Reader")
    
    # Initialize OpenAI model
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8)
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an experienced tarot reader. Answer the user's question basis of 3 cards drawn as the context: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    
    # Initialize output parser
    output_parser = StrOutputParser()
    
    # Chain the components
    chain = prompt | model | output_parser
    
 # Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if current := st.chat_input("Ask your question here?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(current)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": current})
    
    
    # Generate tarot cards
    cards , image_path  = draw_cards()
    st.image(image_path, width = 100)
    st.write("Cards drawn:", cards)
    
    # Create question for the model
    question = current + cards
    context  = """ You are an experienced tarot reader. 
    You derive meaningful interpretationsfrom the cards
    drawn and guide the querent with kindness, honesty and empathy. 
    You refer to the symbolisms and mythology to empower the querent.
    You also provide an overall summary and interpretation."""
    # Invoke the chain
    response = chain.invoke({
        "chat_history": chat_history,
        "context": context ,
        "input": question
    })
    
    # Update chat history
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response))
    
    with st.chat_message("Reader"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "Reader", "content": response})
