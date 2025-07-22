import streamlit as st 
import sqlite3
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Doctor Finder", layout="centered")

st.markdown(
    """
    <style>
        body {
            background-color: #fbf9f6;
        }
        .stApp {
            background-color: #fbf9f6;
        }
    </style>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns([2, 4])

with col1:
    logo = Image.open("testphoto")
    st.image(logo, use_container_width=True)

with col2:
    st.markdown("## Find a Specialist Near You")

conn = sqlite3.connect("PT.db")
cursor = conn.cursor()

df = pd.read_sql("SELECT * FROM doctors", conn)

types = df["type"].unique().tolist()
cities = df["city"].unique().tolist()
specialties = df["specialty"].unique().tolist()
settings = df["setting"].unique().tolist()

st.subheader("Filter by:")
col1, col2 = st.columns(2)

with col1:
    selected_type = st.selectbox("Doctor Type", ["Any"] + types)
    selected_city = st.selectbox("City", ["Any"] + cities)

with col2:
    selected_specialty = st.selectbox("Specialty", ["Any"] + specialties)
    selected_setting = st.selectbox("Care Setting", ["Any"] + settings)

filtered_df = df.copy()

if selected_type != "Any":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]
if selected_city != "Any":
    filtered_df = filtered_df[filtered_df["city"] == selected_city]
if selected_specialty != "Any":
    filtered_df = filtered_df[filtered_df["specialty"] == selected_specialty]
if selected_setting != "Any":
    filtered_df = filtered_df[filtered_df["setting"] == selected_setting]

st.subheader("Matching Doctors:")

if filtered_df.empty:
    st.info("No matching doctors found.")
else:
    for _, row in filtered_df.iterrows():
        with st.expander(f"Dr. {row['name']} ({row['specialty']} - {row['city']})"):
            st.markdown(f"**Practice Type:** {row['type']}")
            st.markdown(f"**Care Setting:** {row['setting']}")
            st.markdown(f"**Address:** {row['address']}")
            st.markdown(f"**Contact Info:** {row['contact_info']}")
            st.markdown(f"**Bio:** {row.get('bio', 'No bio available.')}")

conn.close()
