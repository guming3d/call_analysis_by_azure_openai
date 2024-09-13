import os
import json
import streamlit as st

def display_report():
    st.set_page_config(layout="wide")
    st.title("EF Call Analysis Report")

    output_directory = './output'
    json_files = [f for f in os.listdir(output_directory) if f.endswith('.json')]

    for json_file in json_files:
        file_path = os.path.join(output_directory, json_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        st.subheader(f"Report for {json_file}")
        st.json(data)

if __name__ == "__main__":
    display_report()
