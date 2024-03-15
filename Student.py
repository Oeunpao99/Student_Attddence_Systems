import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Student information
student_info = """
27,e20211015,KHOEM SIVIN,M
28,e20210176,KHON KHENGMENG,M
29,e20211527,KHUN SITHANUT,M
30,e20200497,KONG CHANRAKSA,F
31,e20210963,KONG SATTHA,M
32,e20211537,KONG SEREYRATHA,M
33,e20210574,KOSAL CHANSOTHAY,M
34,e20211754,KOUM SOKNAN,M
35,e20200014,LAB THAVRITH,M
36,e20200413,LENG MOUYHONG,M
37,e20210086,LONG RATANAKVICHEA,M
38,e20210684,LUN CHANPOLY,M
39,e20211077,LY SOKPHENG,M
40,e20210359,MA OUSA,M
41,e20210207,MAK NIMOL,F
42,e20211621,MAO SEDTHA,M
43,e20210249,MORK MONGKUL,M
44,e20210134,NGORN PANHA,M
45,e20210490,NOM MENGHOUY,F
46,e20210635,OEUN PAO,M
47,e20211548,PAV LIMSENG,M
48,e20210072,PEANG RATTANAK,M
49,e20201314,PEL BUNKHLOEM,M
50,e20211572,PEN VIRAK,M
51,e20211154,PHALLY MAKARA,M
52,e20210227,PHAO CHANTHIN,F
"""

# Parse student information into DataFrame
student_data = [line.split(",") for line in student_info.strip().split("\n")]
df_students = pd.DataFrame(student_data, columns=[
                           "Index", "ID", "Name", "Gender"])

# Add attendance status column with initial value "Absence"
df_students["Attendance Status"] = "Absence"

# Function to display student list table


@st.cache(allow_output_mutation=True)
def get_student_df():
    return df_students

# Function to reset the table every 2 minutes


def reset_table():
    # Check if 2 minutes have passed since the last reset
    if "last_reset" not in st.session_state:
        st.session_state["last_reset"] = datetime.now()
    elif datetime.now() - st.session_state["last_reset"] >= timedelta(minutes=2):
        # Reset the table
        st.session_state["last_reset"] = datetime.now()
        df_students["Attendance Status"] = "Absence"

# Main function to run the Streamlit app


def main():
    st.title("Student Attendance System")

    # Reset the table if needed
    reset_table()

    df_students = get_student_df()

    st.sidebar.subheader("Student List")
    # Display the sidebar table here and it will automatically update when df_students is updated
    st.sidebar.table(df_students[["Name", "ID", "Attendance Status"]].style.applymap(
        lambda x: 'color: white' if x.strip() == 'Absence' else 'color: green'))

    st.subheader("Attendance Form")
    student_name = st.text_input("Name:")
    student_id = st.text_input("ID:")

    if st.button("Submit"):
        # Update attendance status to "Present"
        df_students.loc[(df_students["Name"] == student_name) & (
            df_students["ID"] == student_id), "Attendance Status"] = "Present"
        st.success("Attendance submitted successfully.")
        # No need to display the table again, as the sidebar table will automatically update


if __name__ == "__main__":
    main()
