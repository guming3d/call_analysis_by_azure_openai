import os

class FileIngestion:
    def __init__(self, directory: str, logger):
        self.directory = directory
        self.logger = logger
    
    def get_audio_files(self):
        self.logger.info(f"Fetching audio files from: {self.directory}")
        audio_files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) if f.endswith(('.mp3', '.wav'))]
        self.logger.info(f"Found {len(audio_files)} audio files.")
        return audio_files