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
            max-height: 250px;
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
df = pd.read_sql("SELECT * FROM doctors", conn)

# Get unique options (sorted)
types = sorted(df["type"].dropna().unique().tolist(), key=str.lower)
cities = sorted(df["city"].dropna().unique().tolist(), key=str.lower)
specialties = sorted(df["specialty"].dropna().unique().tolist(), key=str.lower)
settings = sorted(df["setting"].dropna().unique().tolist(), key=str.lower)
genders = sorted(df["gender"].dropna().unique().tolist(), key=str.lower)

# Initialize session state if not set
for key in ["selected_type", "selected_city", "selected_specialty", "selected_setting", "selected_gender"]:
    if key not in st.session_state:
        st.session_state[key] = "Any"

# Filter section
st.subheader("Filter by:")
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.selectbox("Clinician Type", ["Any"] + types, key="selected_type")
with col2:
    st.selectbox("City", ["Any"] + cities, key="selected_city")
with col3:
    st.selectbox("Specialty", ["Any"] + specialties, key="selected_specialty")
with col4:
    st.selectbox("Care Setting", ["Any"] + settings, key="selected_setting")
with col5:
    st.selectbox("Gender", ["Any", "Female", "Male"], key="selected_gender")
with col6:
    st.markdown("<br>", unsafe_allow_html=True)  # spacing to align button
    if st.button("Reset Filters"):
        st.session_state.selected_type = "Any"
        st.session_state.selected_city = "Any"
        st.session_state.selected_specialty = "Any"
        st.session_state.selected_setting = "Any"
        st.session_state.selected_gender = "Any"

# Pull current selections from session_state
selected_type = st.session_state.selected_type
selected_city = st.session_state.selected_city
selected_specialty = st.session_state.selected_specialty
selected_setting = st.session_state.selected_setting
selected_gender = st.session_state.selected_gender

# Apply filters
filters_applied = any([
    selected_type != "Any",
    selected_city != "Any",
    selected_specialty != "Any",
    selected_setting != "Any",
    selected_gender != "Any"
])

filtered_df = df.copy()
if selected_type != "Any":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]
if selected_city != "Any":
    filtered_df = filtered_df[filtered_df["city"] == selected_city]
if selected_specialty != "Any":
    filtered_df = filtered_df[filtered_df["specialty"] == selected_specialty]
if selected_setting != "Any":
    filtered_df = filtered_df[filtered_df["setting"] == selected_setting]
if selected_gender != "Any":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]

# Show results only if a filter is applied
if filters_applied:
    if filtered_df.empty:
        st.subheader("Matching Doctors:")
        st.info("No matching doctors found.")
    else:
        st.subheader("Matching Doctors:")
        for _, row in filtered_df.iterrows():
            with st.expander(f"Dr. {row['name']} ({row['specialty']} - {row['city']})"):
                st.markdown(f"**Practice Type:** {row['type']}")
                st.markdown(f"**Care Setting:** {row['setting']}")
                st.markdown(f"**Address:** {row['address']}")
                st.markdown(f"**Contact Info:** {row['contact_info']}")
                st.markdown(f"**Gender:** {row['gender']}")
                st.markdown(f"**Bio:** {row.get('bio', 'No bio available.')}")

conn.close()
