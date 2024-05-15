import random
import pandas as pd
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.output_parsers import StrOutputParser

## load api key
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')



def draw_cards():
    df = pd.read_csv("cards.csv")
    card1 = random.randint(0, 77)
    card2 = random.randint(0, 77)
    while card1 == card2:
        card2 =  random.randint(0, 77)
    card3 = random.randint(0, 77)
    while (card3 == card2 or  card1==card3):
        card2 =  random.randint(0, 77)

    cards_drawn = df.at[card1, 'Name']+ ", " +df.at[card2, 'Name']+ ", " + df.at[card3, 'Name']
    return cards_drawn

if __name__ == "__main__":
    
    
    # Initialize chat history
    chat_history = []
    

    
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system" ,"You are an exprienced tarot reader.\
              Answer the user's question basis of 3 cards\
              drawn as the context: {context}" ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ]
    )
    output_parser =  StrOutputParser()
    chain = prompt | model | output_parser
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        context  = """ You are an experienced tarot reader. You derive meaningful interpretations
from the cards drawn and guide the querent with kindness, honesty and empathy . You 
refer to the symbolisms and mythology to empower the querent. You also provide an overall summary and interpretation."""
        cards = draw_cards()
        print(" cards drawn: ", cards)
        question = user_input + cards

        response = chain.invoke({
        "chat_history": chat_history,
        'context' : context,
        "input": question,})
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))
        print("Tarot Reader:", response)