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

# Get unique filter options (all sorted alphabetically, case-insensitive)
types = sorted(df["type"].dropna().unique().tolist(), key=str.lower)
cities = sorted(df["city"].dropna().unique().tolist(), key=str.lower)
specialties = sorted(df["specialty"].dropna().unique().tolist(), key=str.lower)
settings = sorted(df["setting"].dropna().unique().tolist(), key=str.lower)

# Initialize session state
for key in ["selected_type", "selected_city", "selected_specialty", "selected_setting"]:
    if key not in st.session_state:
        st.session_state[key] = "Any"

# Reset filters
if st.button("Reset Filters"):
    st.session_state.selected_type = "Any"
    st.session_state.selected_city = "Any"
    st.session_state.selected_specialty = "Any"
    st.session_state.selected_setting = "Any"
    st.experimental_rerun()

st.subheader("Filter by:")
col1, col2 = st.columns(2)

with col1:
    st.session_state.selected_type = st.selectbox("Clinician Type", ["Any"] + types, index=(["Any"] + types).index(st.session_state.selected_type))
    st.session_state.selected_city = st.selectbox("City", ["Any"] + cities, index=(["Any"] + cities).index(st.session_state.selected_city))

with col2:
    st.session_state.selected_specialty = st.selectbox("Specialty", ["Any"] + specialties, index=(["Any"] + specialties).index(st.session_state.selected_specialty))
    st.session_state.selected_setting = st.selectbox("Care Setting", ["Any"] + settings, index=(["Any"] + settings).index(st.session_state.selected_setting))

# Apply filters
filters_applied = any([
    st.session_state.selected_type != "Any",
    st.session_state.selected_city != "Any",
    st.session_state.selected_specialty != "Any",
    st.session_state.selected_setting != "Any"
])

filtered_df = df.copy()
if st.session_state.selected_type != "Any":
    filtered_df = filtered_df[filtered_df["type"] == st.session_state.selected_type]
if st.session_state.selected_city != "Any":
    filtered_df = filtered_df[filtered_df["city"] == st.session_state.selected_city]
if st.session_state.selected_specialty != "Any":
    filtered_df = filtered_df[filtered_df["specialty"] == st.session_state.selected_specialty]
if st.session_state.selected_setting != "Any":
    filtered_df = filtered_df[filtered_df["setting"] == st.session_state.selected_setting]

# Show results only if a filter is applied
if filters_applied:
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
else:
    st.info("Use the filters above to find a matching doctor.")

conn.close()
