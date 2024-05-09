import streamlit as st
import random
st.title("tarot reader")
st.write("Tarot reader")



question = st.text_input("Ask your question.")
if question:
    card1 = random.randint(0, 77)
    print(card1)
    card2 = random.randint(0, 77)
    while card1 == card2:
        card2 =  random.randint(0, 77)
    card3 = random.randint(0, 77)
    while (card3 == card2 or  card1==card3):
        card2 =  random.randint(0, 77)
    print(card3)

    image_paths = [f"images/{card1}.png",f"images/{card2}.png",f"images/{card3}.png"]
    st.image(image_paths, width=200)

st.write(question)