import os
from src.file_ingestion import FileIngestion
from src.transcription_service import TranscriptionService
from src.output_generator import OutputGenerator
from src.backend import generate_content_azure 
from src.prompt import generate_system_prompt
from src.logger import Logger
from src.generate_report import generate_report


def main():
    logger = Logger()
    
    # Set directories
    input_directory = './audios'
    output_directory = './output'
    
    # Initialize components
    file_ingestion = FileIngestion(input_directory, logger)
    transcription_service = TranscriptionService(logger)
    output_generator = OutputGenerator(output_directory, logger)
    
    # Process each file
    for audio_file in file_ingestion.get_audio_files():
        try:
            # Check if the result JSON file already exists
            result_json_file = os.path.join(output_directory, os.path.basename(audio_file).replace('.mp3', '.json').replace('.wav', '.json'))
            if os.path.exists(result_json_file):
                logger.info(f"Result JSON file already exists for {audio_file}, skipping transcription and analysis.")
                continue

            # Transcription
            transcription_result = transcription_service.recognize_from_file(audio_file)
            logger.info(f"Transcription Result: {transcription_result}")
            
            # Analysis by Azure OpenAI
            analysis_result = generate_content_azure(generate_system_prompt(), transcription_result, max_tokens=600)
            
            # Output Generation
            output_generator.generate_output(audio_file, analysis_result, transcription_result)
        except Exception as e:
            logger.error(f"Error processing {audio_file}: {e}")

    # Generate report
    generate_report(output_directory, 'report.xlsx', 'report.md')

if __name__ == "__main__":
    main()
