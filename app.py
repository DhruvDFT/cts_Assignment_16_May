import streamlit as st
from powerplan_set1 import questions as set1
from powerplan_set2 import questions as set2
from powerplan_set3 import questions as set3
from powerplan_set4 import questions as set4

def main():
    st.title("PowerPlan + TCL Assignment Questions")
    option = st.sidebar.selectbox("Select Question Set", ["Set 1", "Set 2", "Set 3", "Set 4"])
    qs = {"Set 1": set1, "Set 2": set2, "Set 3": set3, "Set 4": set4}[option]
    for idx, q in enumerate(qs, start=1):
        st.markdown(f"**Q{idx}.** {q}")

if __name__ == "__main__":
    main()