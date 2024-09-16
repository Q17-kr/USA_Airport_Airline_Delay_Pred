import streamlit as st
import os
import datetime as dt
import pandas as pd

st.session_state["change"] = False

def split_description(description):
    parts = description.split(": ")
    return parts[1] if len(parts) > 1 else description

Input = st.form("in")

with Input:
    date = st.date_input("출발 날짜", "today", dt.date.today(), help="현 날짜로부터 3일 이후의 예측은 정확도가 떨어질 수 있습니다.")

    time = st.time_input("출발 시각", dt.time(0), step=dt.timedelta(hours=1))
    
    airlines = {
        "Alaska Airlines Inc. (AS)": 319,
        "Allegiant Air (G4)": 684,
        "American Airlines Inc. (AA)": 187,
        "Delta Air Lines Inc. (DL)": 552,
        "Endeavor Air Inc. (9E)": 170,
        "Envoy Air (MQ)": 1021,
        "Frontier Airlines Inc. (F9)": 637,
        "Hawaiian Airlines Inc. (HA)": 753,
        "JetBlue Airways (B6)": 361,
        "PSA Airlines Inc. (OH)": 1120,
        "Republic Airline (YX)": 1706,
        "SkyWest Airlines Inc. (OO)": 1135,
        "Southwest Airlines Co. (WN)": 1615,
        "Spirit Air Lines (NK)": 1084,
        "United Air Lines Inc. (UA)": 1511
    }
    airline = st.selectbox("이용 항공사", ["항공사 선택"] + list(airlines.keys()), 0)
    try:
        airline = airlines[airline]
    except:
        pass

    ports = pd.read_csv(os.path.join("data", "airportID.csv")).drop("Unnamed: 0", axis=1)
    ports['Description'] = ports["Description"].apply(split_description)

    originPort = st.selectbox("출발 공항", [
        "공항 선택",
        "Chicago O'Hare International",
        "Dallas/Fort Worth International",
        "Denver International",
        "Hartsfield-Jackson Atlanta International",
        "Los Angeles International"
        ], 0, help="현재 출발 공항은 5개만 설정 가능합니다.")
    st.session_state["origin"] = originPort
    originPort = ports.loc[ports["Description"] == originPort, "index"]

    destPort = st.selectbox("도착 공항", ["공항 선택"] + list(ports["Description"]), 0)
    st.session_state["dest"] = destPort
    destPort = ports.loc[ports["Description"] == destPort, "index"]
    
    airtime = st.time_input("예상 비행시간", dt.time(0), step=dt.timedelta(minutes=10))
    
    if st.form_submit_button("예측하기"):
        if airline == "항공사 선택" \
        or len(originPort) == 0 \
        or len(destPort) == 0 \
        or (airtime.hour == 0 and airtime.minute == 0):
            st.error("입력되지 않은 값이 있습니다.")
        else:
            st.session_state["data"] = pd.DataFrame({
                'month': [date.month, 1],
                'day': [date.day, 1],
                'dayWeek': [date.weekday(), 0],
                'airlineId': [airline, 0],
                'originPortId': [originPort.iloc[0], 0],
                'destPortId': [destPort.iloc[0], 0],
                'planedDepHour': [time.hour, 0],
                'airTime': [(airtime.hour * 60) + airtime.minute, 0]
            })
            
            st.session_state["change"] = True
