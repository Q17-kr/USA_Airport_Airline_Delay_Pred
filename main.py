import streamlit as st
import os

if "data" not in st.session_state:
    st.session_state["data"] = []
    st.session_state["change"] = True

st.title("미국 항공 지연 예측")
st.write(" ")
st.write(" ")

Input = st.Page(os.path.join("data","input.py"))
result = st.Page(os.path.join("data","result.py"))

menu = st.navigation([Input, result], position="hidden")

menu.run()

if st.session_state["change"]:
    if len(st.session_state["data"]) == 0:
        st.switch_page(Input)
    else:
        st.switch_page(result)