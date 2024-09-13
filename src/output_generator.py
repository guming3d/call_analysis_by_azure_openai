import json
import os

class OutputGenerator:
    def __init__(self, directory: str, logger):
        self.directory = directory
        self.logger = logger
    
    def generate_output(self, audio_file: str, analysis_result: str, transcribed_content: str):
        output_file = os.path.join(self.directory, os.path.basename(audio_file).replace('.mp3', '.json').replace('.wav', '.json'))
        self.logger.info(f"Generating output file: {output_file}")
        
        output_data = {
            "call_id": os.path.basename(audio_file),
            "analysis_result": analysis_result,
            "transcribed_content": transcribed_content
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=4)
        
        self.logger.info(f"Output file created: {output_file}")
