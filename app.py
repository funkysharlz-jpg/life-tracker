import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- APP CONFIG ---
st.set_page_config(page_title="Life Tracker", layout="wide")
DATA_FILE = "life_tracker_data.csv"

# --- DATA STRUCTURE ---
categories = {
    "Overall wellbeing & actions": ["What was my overall wellbeing?", "Was I the person I want to be?"],
    "Faith": ["Did I engage in spiritual practices?"],
    "Relationships & community": ["Did I love my partner well?", "Did I love my family well?", "Did I love my friends well?", "Did I contribute to society / the community?"],
    "Mental health": ["Did I do my morning routine?", "How did I handle stress?", "Did I spend 5+ minutes on mental health?"],
    "Physical health": ["How did I feel physically?", "How many hours of sleep did I get?", "What was the quality of my sleep?", "Did I eat healthy?", "Did I work out?"],
    "Work": ["Did I enjoy work?", "How many hours did I work?", "Was I wise financially?"],
    "Purpose & engagement": ["Did I experience meaning?", "Did I experience positive emotions?", "Did I feel engaged by what I was doing?"],
    "Achievement & growth": ["Did I have a sense of achievement?", "Was my mind stimulated / did I learn?", "Did I achieve my daily goals?"],
    "Character & virtue": ["Did I practice the virtues I am working on?", "Was I of service or generous to others?", "Did I practice the habits I am building?"],
    "Entertainment": ["Was my engagement in hobbies & entertainment healthy?"]
}

# --- HELPER FUNCTIONS ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Date"] + [q for sub in categories.values() for q in sub])

def save_entry(entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# --- UI ---
st.title("Daily Life Tracker")

tab1, tab2 = st.tabs(["Log Daily Entry", "View Insights"])

with tab1:
    st.header(f"Entry for {datetime.now().strftime('%Y-%m-%d')}")
    new_entry = {"Date": datetime.now().strftime('%Y-%m-%d')}
    
    for cat, questions in categories.items():
        with st.expander(cat):
            for q in questions:
                if "hours" in q.lower():
                    new_entry[q] = st.number_input(q, min_value=0.0, max_value=24.0, step=0.5)
                else:
                    new_entry[q] = st.select_slider(q, options=[1, 2, 3, 4, 5], value=3)
    
    if st.button("Submit Entry"):
        save_entry(new_entry)
        st.success("Entry Saved!")

with tab2:
    df = load_data()
    if not df.empty:
        st.header("Your Progress")
        selected_q = st.selectbox("Select a metric to view:", df.columns[1:])
        
        # Color-coded Bar Chart
        fig = px.bar(df, x="Date", y=selected_q, 
                     color=selected_q, 
                     color_continuous_scale='RdYlGn',
                     title=f"Trend for: {selected_q}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data logged yet.")
