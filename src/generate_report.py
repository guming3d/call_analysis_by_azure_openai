import os
import json
import pandas as pd

def generate_report(output_directory: str, excel_file: str, markdown_file: str):
    data = []

    # Collect data from JSON files
    for file_name in os.listdir(output_directory):
        if file_name.endswith('.json'):
            with open(os.path.join(output_directory, file_name), 'r', encoding='utf-8') as f:
                content = json.load(f)
                data.append([
                    content.get("call_id", ""),
                    content.get("transcribed_content", ""),
                    content.get("analysis_result", "")
                ])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=["Audio File", "Transcription Result", "Analysis Result"])

    # Save to Excel
    df.to_excel(excel_file, index=False)

    # Save to Markdown
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(df.to_markdown(index=False))

    print(f"Report generated: {excel_file} and {markdown_file}")