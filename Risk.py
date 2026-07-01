
import requests
import streamlit as st
from datetime import date
import sqlite3
import joblib
import re

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Health Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load(open("health_model.pkl", "rb"))

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #f4f8fb;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0E76A8, #0A4F70);
}

[data-testid="stSidebar"] * {
    color: white;
}

.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #0E76A8;
    text-align: center;
    margin-bottom: 10px;
}

.sub-title {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.metric-card {
    background: linear-gradient(135deg, #0E76A8, #3BAFDA);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
}

.metric-label {
    font-size: 16px;
}

.stButton button {
    width: 100%;
    background: linear-gradient(90deg, #0E76A8, #3BAFDA);
    color: white;
    border: none;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    font-weight: bold;
}

.stButton button:hover {
    background: linear-gradient(90deg, #0A4F70, #0E76A8);
    color: white;
}

.result-box {
    background-color: #E8F6EF;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #28A745;
    margin-top: 20px;
}

.high-risk {
    background-color: #FDEDEC;
    border-left: 6px solid red;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# CREATE DATABASE
# =====================================================

conn = sqlite3.connect("health_app.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patient_records (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    haemoglobin REAL,
    cholesterol REAL,
    prediction TEXT

)
""")

conn.commit()

conn.close()

# =====================================================
# TITLE
# =====================================================

st.markdown("""
<div class='main-title'>
🩺 Health Prediction Application
</div>

<div class='sub-title'>
AI Based Disease Prediction System
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# SESSION PAGE
# =====================================================

if "page" not in st.session_state:

    st.session_state.page = "Dashboard"

# =====================================================
# SIDEBAR MENU
# =====================================================

pages = [
    "Dashboard",
    "Patient Entry",
    "Patient Records"
]

menu = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(st.session_state.page)
)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    # st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📊 Dashboard")

    conn = sqlite3.connect("health_app.db")

    cursor = conn.cursor()
# ===============================================
    cursor.execute(
        "SELECT COUNT(*) FROM patient_records"
    )
    total_patients = cursor.fetchone()[0]
# ===============================================
    cursor.execute("""
                    SELECT COUNT(*) FROM patient_records WHERE prediction LIKE '%Diabetes%' """) 
    diabetes_count = cursor.fetchone()[0]
    # ========================================================================
    cursor.execute(""" SELECT COUNT(*) FROM patient_records WHERE prediction LIKE '%Anemia%' """)
    anemia_count = cursor.fetchone()[0]
    # =============================================================================
    cursor.execute(""" SELECT COUNT(*) FROM patient_records WHERE prediction LIKE '%Heart%' """) 
    heart_count = cursor.fetchone()[0]
    # ==========================================================================
    

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
                    <div class='metric-card'> 
                    <div class='metric-title'> Total Patients </div> 
                    <div class='metric-value'> {total_patients} </div> 
                    </div> """, unsafe_allow_html=True)
    with col2:

        st.markdown(f"""
                    <div class='metric-card'> 
                    <div class='metric-title'> Diabetes Patients </div> 
                    <div class='metric-value'> {diabetes_count} </div> 
                    </div> """, unsafe_allow_html=True)
    with col3:

        st.markdown(f"""
                    <div class='metric-card'> 
                    <div class='metric-title'> Anemia Patients </div> 
                    <div class='metric-value'> {anemia_count} </div> 
                    </div> """, unsafe_allow_html=True)
    with col4:

        st.markdown(f"""
                    <div class='metric-card'> 
                    <div class='metric-title'> Heart Patients </div> 
                    <div class='metric-value'> {heart_count} </div> 
                    </div> """, unsafe_allow_html=True)  
    conn.close()

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PATIENT ENTRY PAGE
# =====================================================

elif menu == "Patient Entry":

    # st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("➕ Patient Health Entry Form")

    # =====================================================
    # EDIT MODE VALUES
    # =====================================================

    edit_mode = "edit_id" in st.session_state

    default_name = st.session_state.get(
        "edit_name",
        ""
    )

    default_dob = st.session_state.get(
        "edit_dob",
        date.today()
    )

    if isinstance(default_dob, str):

        default_dob = date.fromisoformat(default_dob)

    default_email = st.session_state.get(
        "edit_email",
        ""
    )

    default_glucose = st.session_state.get(
        "edit_glucose",
        0.0
    )

    default_haemoglobin = st.session_state.get(
        "edit_haemoglobin",
        0.0
    )

    default_cholesterol = st.session_state.get(
        "edit_cholesterol",
        0.0
    )

    # =====================================================
    # FORM
    # =====================================================

    with st.form("health_form"):

        full_name = st.text_input(
            "Full Name",
            value=default_name,
            placeholder="Enter full name"
        )

        dob = st.date_input(
            "Date of Birth",
            value=default_dob,
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

        email = st.text_input(
            "Email Address",
            value=default_email,
            placeholder="Enter email address"
        )

        # =====================================================
        # HEALTH VALUES
        # =====================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            glucose = st.number_input(
                "Glucose",
                min_value=0.0,
                max_value=10.0,
                value=float(default_glucose),
                step=0.1,
                format="%.1f"
            )

        with col2:

            haemoglobin = st.number_input(
                "Haemoglobin",
                min_value=0.0,
                max_value=20.0,
                value=float(default_haemoglobin),
                step=0.1,
                format="%.1f"
            )

        with col3:

            cholesterol = st.number_input(
                "Cholesterol",
                min_value=0.0,
                value=float(default_cholesterol),
                step=1.0
            )

        # =====================================================
        # BUTTON
        # =====================================================

        if edit_mode:

            submit_button = st.form_submit_button(
                "🔄 Update Prediction"
            )

        else:

            submit_button = st.form_submit_button(
                "Predict"
            )

    # =====================================================
    # VALIDATION + PREDICTION
    # =====================================================

    if submit_button:

        validation_passed = True

        # =====================================================
        # NAME VALIDATION
        # =====================================================

        if full_name.strip() == "":

            st.error(
                "Full Name is required."
            )

            validation_passed = False

        elif not full_name.replace(" ", "").isalpha():

            st.error(
                "Full Name should contain only alphabets."
            )

            validation_passed = False

        # =====================================================
        # EMAIL VALIDATION
        # =====================================================

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):

            st.error(
                "Please enter valid email address."
            )

            validation_passed = False

       
        # =====================================================
        # MODEL PREDICTION
        # =====================================================

        if validation_passed:

            payload = {

                "glucose": glucose,
                "haemoglobin": haemoglobin,
                "cholesterol": cholesterol

            }

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=payload
                )

                result = response.json()

                prediction_result = result["prediction"]

                st.session_state.prediction_done = True

                st.session_state.prediction_result = prediction_result

            except Exception as e:

                st.error(
                    f"API Connection Error: {e}"
                )



    # =====================================================
    # DISPLAY RESULT
    # =====================================================

    if st.session_state.get("prediction_done", False):

        prediction_result = st.session_state.prediction_result

        if prediction_result.lower() == "healthy":

            result_class = ""

        else:

            result_class = "high-risk"

        st.markdown(
            f"""
<div class='result-box {result_class}'>

<h3>Prediction Result</h3>

<h2>{prediction_result}</h2>

<p>
AI model prediction generated successfully.
</p>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================================
        # UPDATE BUTTON
        # =====================================================

        if edit_mode:

            if st.button("🔄 Update Record"):

                conn = sqlite3.connect("health_app.db")

                cursor = conn.cursor()

                cursor.execute("""
                UPDATE patient_records
                SET
                    full_name = ?,
                    dob = ?,
                    email = ?,
                    glucose = ?,
                    haemoglobin = ?,
                    cholesterol = ?,
                    prediction = ?
                WHERE id = ?
                """, (

                    full_name,
                    str(dob),
                    email,
                    glucose,
                    haemoglobin,
                    cholesterol,
                    prediction_result,
                    st.session_state.edit_id

                ))

                conn.commit()

                conn.close()

                st.success(
                    "Patient record updated successfully."
                )

                # CLEAR SESSION

                keys_to_remove = [

                    "edit_id",
                    "edit_name",
                    "edit_dob",
                    "edit_email",
                    "edit_glucose",
                    "edit_haemoglobin",
                    "edit_cholesterol",
                    "prediction_done",
                    "prediction_result"

                ]

                for key in keys_to_remove:

                    if key in st.session_state:

                        del st.session_state[key]

                st.session_state.page = "Patient Records"

                st.rerun()

        # =====================================================
        # SAVE BUTTON
        # =====================================================

        else:

            if st.button("💾 Save Details"):

                conn = sqlite3.connect("health_app.db")

                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO patient_records (

                    full_name,
                    dob,
                    email,
                    glucose,
                    haemoglobin,
                    cholesterol,
                    prediction

                )

                VALUES (?, ?, ?, ?, ?, ?, ?)

                """, (

                    full_name,
                    str(dob),
                    email,
                    glucose,
                    haemoglobin,
                    cholesterol,
                    prediction_result

                ))

                conn.commit()

                conn.close()

                st.success(
                    "Patient details saved successfully."
                )

                # =====================================================
                # CLEAR SESSION AFTER SAVE
                # =====================================================

                keys_to_remove = [

                    "prediction_done",
                    "prediction_result"

                ]

                for key in keys_to_remove:

                    if key in st.session_state:

                        del st.session_state[key]

                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PATIENT RECORDS PAGE
# =====================================================

elif menu == "Patient Records":

    # st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📋 Patient Records")

    conn = sqlite3.connect("health_app.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        prediction
    FROM patient_records
    """)

    records = cursor.fetchall()

    # =====================================================
    # TABLE HEADER
    # =====================================================

    header = st.columns([0.7,2,1,1,1.3,2.2,2])

    header[0].markdown("**ID**")
    header[1].markdown("**Name**")
    header[2].markdown("**Glucose**")
    header[3].markdown("**Hb**")
    header[4].markdown("**Cholesterol**")
    header[5].markdown("**Prediction**")
    header[6].markdown("**Actions**")

    st.markdown("---")

    # =====================================================
    # DISPLAY RECORDS
    # =====================================================

    for row in records:

        cols = st.columns([0.7,2,1,1,1.3,2.2,2])

        cols[0].write(row[0])

        cols[1].write(row[1])

        cols[2].write(row[4])

        cols[3].write(row[5])

        cols[4].write(row[6])

        cols[5].write(row[7])

        # =====================================================
        # ACTION BUTTONS
        # =====================================================

        action1, action2 = cols[6].columns(2)

        # EDIT BUTTON

        with action1:

            if st.button(
                "✏️",
                key=f"edit_{row[0]}"
            ):

                st.session_state.edit_id = row[0]

                st.session_state.edit_name = row[1]

                st.session_state.edit_dob = row[2]

                st.session_state.edit_email = row[3]

                st.session_state.edit_glucose = row[4]

                st.session_state.edit_haemoglobin = row[5]

                st.session_state.edit_cholesterol = row[6]

                st.session_state.page = "Patient Entry"

                st.rerun()

        # DELETE BUTTON

        with action2:

            if st.button(
                "🗑",
                key=f"delete_{row[0]}"
            ):

                cursor.execute(
                    "DELETE FROM patient_records WHERE id = ?",
                    (row[0],)
                )

                conn.commit()

                st.success(
                    "Record deleted successfully."
                )

                st.rerun()

        st.markdown("---")

    conn.close()

    st.markdown("</div>", unsafe_allow_html=True)

