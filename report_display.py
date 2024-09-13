import streamlit as st

def display_report():
    st.title("EF Call Analysis Report")

    with open("report.md", "r", encoding="utf-8") as file:
        report_content = file.read()

    st.markdown(report_content)

if __name__ == "__main__":
    display_report()
