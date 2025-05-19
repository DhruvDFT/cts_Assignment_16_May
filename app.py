import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Define the questions modules
from powerplan_set1 import questions as set1
from powerplan_set2 import questions as set2
from powerplan_set3 import questions as set3
from powerplan_set4 import questions as set4

# Responses storage
RESPONSES_FILE = "responses.csv"

# Determine if admin view
query_params = st.experimental_get_query_params()
is_admin = query_params.get("admin", ["0"])[0] == "1"

# Sidebar selection
st.sidebar.title("Controls")
selected_set = st.sidebar.selectbox(
    "Choose Question Set:",
    ["Set 1", "Set 2", "Set 3", "Set 4"]
)
qs_map = {"Set 1": set1, "Set 2": set2, "Set 3": set3, "Set 4": set4}
qs = qs_map[selected_set]

if is_admin:
    st.title("📊 Download Submissions")
    if os.path.exists(RESPONSES_FILE):
        df = pd.read_csv(RESPONSES_FILE)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download all responses as CSV",
            data=csv,
            file_name="responses.csv",
            mime="text/csv"
        )
    else:
        st.info("No submissions yet.")
else:
    st.title(f"{selected_set} - PowerPlan + TCL Answers")
    with st.form("answer_form", clear_on_submit=True):
        student = st.text_input("Your Name")
        email = st.text_input("Your Email")
        responses = []
        for idx, q in enumerate(qs, start=1):
            responses.append(st.text_area(f"Q{idx}. {q}", key=f"resp_{idx}"))
        submit = st.form_submit_button("Submit Answers")

        if submit:
            if not student:
                st.error("Please enter your name before submitting.")
            elif not email:
                st.error("Please enter your email before submitting.")
            else:
                # Build row with dynamic question columns
                row = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "student": student,
                    "email": email,
                    "set": selected_set
                }
                for idx, (q, answer) in enumerate(zip(qs, responses), start=1):
                    row[f"Q{idx}: {q}"] = answer

                # Append to CSV
                if os.path.exists(RESPONSES_FILE):
                    df = pd.read_csv(RESPONSES_FILE)
                    df = df.append(row, ignore_index=True)
                else:
                    df = pd.DataFrame([row])

                df.to_csv(RESPONSES_FILE, index=False)
                st.success("Your answers have been submitted!")

    st.markdown("---")
    st.write("After submitting, please close this tab. Thank you!")