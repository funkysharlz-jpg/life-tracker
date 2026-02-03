import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Good Life Tracker", layout="wide")

# --- SECURE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- EXACT DATA STRUCTURE FROM YOUR UPDATED FILE ---
data_structure = {
    "Overall wellbeing & actions": [
        "What was my overall wellbeing?", 
        "Was I the person I want to be?"
    ],
    "Relationships & community": [
        "Did I love my partner well?", 
        "Did I spend quality time with Caris?", 
	"Did I spend quality time with Zara?", 
        "Did I love my friends well?", 
        "Did I contribute to society / the community?"
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
    "Work": [
        "Did I enjoy work?", 
        "How many hours did I work?", 
        "Was I wise financially?"
    ],
    "Purpose & engagement": [
        "Did I experience meaning?", 
        "Did I experience positive emotions?", 
        "Did I feel engaged by what I was doing?"
    ],
    "Achievement & growth": [
        "Did I have a sense of achievement?", 
        "Was my mind stimulated / did I learn?", 
        "Did I achieve my daily goals?"
    ],
    "Character & virtue": [
        "Did I practice the virtues (kindness, patience) I am working on?", 
        "Was I of service or generous to others?", 
        "Did I practice gratitude today?"
    ],
    "Entertainment": [
        "Did I read today?", 
	"Did I do some cross stitch today?"
    ]
}

all_qs = [q for sub in data_structure.values() for q in sub]

st.title("🌟 Good Life Tracker")

tab1, tab2 = st.tabs(["📝 Daily Entry", "📈 View Trends"])

with tab1:
    # Adding a clear_on_submit to reset the form after saving
    with st.form("entry_form", clear_on_submit=True):
        date_val = st.date_input("Date", datetime.now())
        entry = {"Date": date_val.strftime('%Y-%m-%d')}
        
        for category, questions in data_structure.items():
            st.markdown(f"### {category}")
            for q in questions:
                # Logic to determine input type based on the question text
                if "hours" in q.lower():
                    entry[q] = st.number_input(q, min_value=0.0, max_value=24.0, step=0.5, key=q)
                else:
                    entry[q] = st.select_slider(q, options=[1, 2, 3, 4, 5], value=3, key=q)
            st.divider()
        
        submit = st.form_submit_button("Submit Daily Reflection")
        
        if submit:
            try:
                # Read current data and append
                existing_df = conn.read()
                new_row = pd.DataFrame([entry])
                updated_df = pd.concat([existing_df, new_row], ignore_index=True)
                
                # Push back to Google Sheets
                conn.update(data=updated_df)
                st.success("Reflections securely saved to your Google Sheet!")
                st.balloons()
            except Exception as e:
                st.error(f"Save failed. Check your Secrets and Permissions: {e}")

with tab2:
    try:
        df_viz = conn.read()
        if not df_viz.empty:
            st.subheader("Visual History")
            target_q = st.selectbox("Select metric to view:", all_qs)
            
            # Color-coded Bar Chart
            fig = px.bar(
                df_viz, 
                x="Date", 
                y=target_q, 
                color=target_q,
                color_continuous_scale='RdYlGn',
                labels={target_q: "Score / Hours"},
                title=f"Trend for: {target_q}"
            )
            
            # Formatting for 1-5 scales vs Hours
            if "hours" not in target_q.lower():
                fig.update_layout(yaxis_range=[0, 5.5])
                
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Your spreadsheet is currently empty. Submit an entry to see charts!")
    except:
        st.warning("Please ensure your Google Sheet is shared with the client email and Secrets are set.")
