import streamlit as st

# List of image paths
i = 1
image_paths = [f"images\{i}.png",f"images\{i+34}.png" , f"images\{i+4}.png"]

for image_path in image_paths:
    st.image(image_path, width=150)  # Adjust width as needed
    st.write("<style>div.row-widget.stHorizontal {flex-wrap: nowrap;}</style>", unsafe_allow_html=True)
