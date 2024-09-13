from src.file_ingestion import FileIngestion
from src.transcription_service import TranscriptionService
from src.output_generator import OutputGenerator
from src.backend import generate_content_azure 
from src.prompt import generate_system_prompt
from src.logger import Logger


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
            # Transcription
            transcription_result = transcription_service.recognize_from_file(audio_file)
            logger.info(f"Transcription Result: {transcription_result}")
            
            # Analysis by Azure OpenAI
            analysis_result = generate_content_azure(generate_system_prompt(), transcription_result, max_tokens=600)
            
            # Output Generation
            output_generator.generate_output(audio_file, analysis_result)
        except Exception as e:
            logger.error(f"Error processing {audio_file}: {e}")

if __name__ == "__main__":
    main()