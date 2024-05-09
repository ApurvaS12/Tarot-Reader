import pandas as pd

df = pd.read_csv("cards.csv")



def get_reading(card1,card2,card3,question):
    cards_drawn = df.at[card1, 'Name']+ " " +df.at[card2, 'Name']+ " " + df.at[card3, 'Name']
    result = (f"You have drawn: {cards_drawn} as the answer to your question")
    return result

if __name__ == "__main__":
    print(get_reading(0,0,0,"calling from backend"))