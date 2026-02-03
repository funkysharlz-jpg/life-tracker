import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Good Life Tracker", layout="wide")

# --- SECURE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- UPDATED CATEGORIES FROM YOUR FILE ---
categories = {
    "Overall wellbeing & actions": ["What was my overall wellbeing?", "Was I the person I want to be?", "Did I feel engaged by what I was doing?", "Was I the person I want to be?"],
    "Relationships & community": [
        "Did I love my partner well?", 
        "Did I spend enough time with Caris?", 
        "Did I spend enough time with Zara?", 
        "Did I love my friends well?"
    ],
    "Mental health": [
        "How did I handle stress?", 
        "Did I spend 5+ minutes on mental health?"
    ],
    "Physical health": [
        "How did I feel physically?", 
        "How many hours of sleep did I get?", 
        "What was the quality of my sleep?", 
        "Did I eat healthy?", 
        "Did I work out?"
    ],
    "Work": ["Did I enjoy work?", "How many hours did I work?", "Was I wise financially?", "Was my mind stimulated / did I learn?", ],
    "Purpose & engagement": [
        "Did I experience meaning?", 
        "Did I experience positive emotions?", 
        "Did I feel engaged by what I was doing?"
    ],
    "Character & virtue": [
        "Did I practice the virtues (patience, kindness) I am working on?", 
        "Did I practice the gratitude today?"
    ],
    "Entertainment": ["Did I read today?", "Did I do some cross stitch today? "]
}

all_qs = [q for sub in categories.values() for q in sub]

st.title("🌟 Good Life Tracker")

tab1, tab2 = st.tabs(["Daily Entry", "Trends & Charts"])

with tab1:
    with st.form("entry_form"):
        date_entry = st.date_input("Date", datetime.now())
        entry_data = {"Date": date_entry.strftime('%Y-%m-%d')}
        
        for cat, qs in categories.items():
            st.subheader(cat)
            for q in qs:
                if "hours" in q.lower():
                    entry_data[q] = st.number_input(q, min_value=0.0, max_value=24.0, step=0.5)
                else:
                    entry_data[q] = st.select_slider(q, options=[1,2,3,4,5], value=3)
        
        if st.form_submit_button("Save Entry"):
            try:
                # Read current data and append
                df = conn.read()
                new_row = pd.DataFrame([entry_data])
                df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=df)
                st.success("Entry securely saved to Google Sheets!")
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    data = conn.read()
    if not data.empty:
        metric = st.selectbox("View progress for:", all_qs)
        fig = px.line(data, x="Date", y=metric, markers=True, 
                      color_discrete_sequence=["#00CC96"])
        st.plotly_chart(fig, use_container_width=True)
