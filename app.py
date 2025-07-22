import streamlit as st 
import sqlite3
import pandas as pd
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(page_title="Doctor Finder", layout="centered")

# Set background color
st.markdown(
    """
    <style>
        body {
            background-color: #fbf9f6;
        }
        .stApp {
            background-color: #fbf9f6;
        }
        .header-container {
            display: flex;
            align-items: center;
            gap: 40px;
            margin-bottom: 20px;
        }
        .header-container img {
            max-height: 300px;
            width: auto;
        }
        .header-title {
            font-size: 32px;
            font-weight: 600;
            color: #2e2e2e;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load logo and convert to base64
logo = Image.open("testphoto")
buffer = BytesIO()
logo.save(buffer, format="PNG")
logo_b64 = base64.b64encode(buffer.getvalue()).decode()

# Display header
st.markdown(
    f"""
    <div class="header-container">
        <img src="data:image/png;base64,{logo_b64}">
        <div class="header-title">Find a Specialist Near You</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Connect to database
conn = sqlite3.connect("PT.db")
cursor = conn.cursor()
df = pd.read_sql("SELECT * FROM doctors", conn)

# Filter options
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

# Apply filters
filtered_df = df.copy()
if selected_type != "Any":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]
if selected_city != "Any":
    filtered_df = filtered_df[filtered_df["city"] == selected_city]
if selected_specialty != "Any":
    filtered_df = filtered_df[filtered_df["specialty"] == selected_specialty]
if selected_setting != "Any":
    filtered_df = filtered_df[filtered_df["setting"] == selected_setting]

# Show results
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
