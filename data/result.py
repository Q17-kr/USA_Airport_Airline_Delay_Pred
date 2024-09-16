import os
import streamlit as st
import lightgbm as lgbm

st.session_state["change"] = False

data = st.session_state["data"].iloc[0]

st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")

st.markdown(f"##### {data[0]}월 {data[1]}일 {data[6]}시경 {st.session_state['origin']}에서 출발하는 비행기의")

model = lgbm.Booster(model_file=os.path.join("data","testmodel.txt"))

result = model.predict(st.session_state["data"])[0]

st.markdown(f"#### 지연 확률은 {result * 100:.1f}%")

if st.button("다른 항공편 예측하기"):
    st.session_state["data"] = []
    st.session_state["change"] = True
