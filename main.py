import os
import sys
import argparse
from src.file_ingestion import FileIngestion
from src.transcription_service import TranscriptionService
from src.output_generator import OutputGenerator
from src.backend import generate_content_azure 
from src.prompt import generate_system_prompt
from src.logger import Logger
from src.generate_report import generate_report

# test:


def main():
    parser = argparse.ArgumentParser(description="Process audio files.")
    parser.add_argument('--replay', action='store_true', help="Use existing transcriptions from the 'transcription' directory.")
    args = parser.parse_args()

    logger = Logger()

    # Check .env file
    from src.backend import check_env_file
    env_valid, env_error = check_env_file()
    if not env_valid:
        logger.error(env_error)
        sys.exit(1)
    
    # Set directories
    input_directory = './audios'
    output_directory = './output'
    transcription_directory = './transcription'
    
    # Ensure directories exist
    os.makedirs(input_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(transcription_directory, exist_ok=True)

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

            transcription_file = os.path.join(transcription_directory, os.path.basename(audio_file).replace('.mp3', '.txt').replace('.wav', '.txt'))
            
            if os.path.exists(transcription_file):
                with open(transcription_file, 'r') as file:
                    transcription_result = file.read()
                logger.info(f"Loaded Transcription Result from file: {transcription_file}")
            elif args.replay:
                # Read transcription from file
                with open(transcription_file, 'r') as file:
                    transcription_result = file.read()
                logger.info(f"Loaded Transcription Result from file: {transcription_file}")
            else:
                # Transcription
                transcription_result = transcription_service.recognize_from_file(audio_file)
                logger.info(f"Transcription Result: {transcription_result}")

                # Save transcription to file
                transcription_file = os.path.join(transcription_directory, os.path.basename(audio_file).replace('.mp3', '.txt').replace('.wav', '.txt'))
                with open(transcription_file, 'w') as file:
                    file.write(transcription_result)
                logger.info(f"Saved Transcription Result to file: {transcription_file}")

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
