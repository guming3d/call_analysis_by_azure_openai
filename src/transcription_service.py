import os
import time
from pydub import AudioSegment
from dotenv import load_dotenv

import azure.cognitiveservices.speech as speechsdk

class TranscriptionService:
    def __init__(self, logger):
        self.logger = logger
        load_dotenv()

        subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY")
        region = os.getenv("AZURE_REGION")

        self.speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        self.speech_config.request_word_level_timestamps()
        # self.speech_config.set_property_by_name("SpeechServiceResponse_SpeakerDiarizationEnabled", "True")
        # self.speech_config.set_property_by_name("SpeechServiceResponse_SpeakerCount", "2")
        self.speech_config.EnableDiarization = True;
        self.speech_config.DiarizationNumberOfSpeakers = 2;
        
        self.speech_config.enable_dictation()
    
    def recognize_from_file(self,  audio_file: str ):
        original_audio_file = audio_file
        if audio_file.endswith('.mp3'):
            wav_file = audio_file.replace('.mp3', '.wav')
            AudioSegment.from_mp3(audio_file).export(wav_file, format='wav')
            audio_file = wav_file

        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
        conversation_transcriber = speechsdk.transcription.ConversationTranscriber(speech_config=self.speech_config, language='zh-CN',audio_config=audio_config)

        transcribing_stop = False
        all_recognized_text = []  # List to store all recognized text

        def conversation_transcriber_recognition_canceled_cb(evt: speechsdk.SessionEventArgs):
            print('Canceled event')

        def conversation_transcriber_session_stopped_cb(evt: speechsdk.SessionEventArgs):
            print('SessionStopped event')

        def conversation_transcriber_transcribed_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            # print('TRANSCRIBED:')
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                # print('\tSpeaker ID={}'.format(evt.result.speaker_id))
                all_recognized_text.append(evt.result.speaker_id + ":")
                # print('\tText={}'.format(evt.result.text))
                all_recognized_text.append(evt.result.text + "\n\n")
            elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                print('\tNOMATCH: Speech could not be TRANSCRIBED: {}'.format(evt.result.no_match_details))

        def conversation_transcriber_session_started_cb(evt: speechsdk.SessionEventArgs):
            print('SessionStarted event')

        def stop_cb(evt: speechsdk.SessionEventArgs):
            #"""callback that signals to stop continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            nonlocal transcribing_stop
            transcribing_stop = True

        # Connect callbacks to the events fired by the conversation transcriber
        conversation_transcriber.transcribed.connect(conversation_transcriber_transcribed_cb)
        conversation_transcriber.session_started.connect(conversation_transcriber_session_started_cb)
        conversation_transcriber.session_stopped.connect(conversation_transcriber_session_stopped_cb)
        conversation_transcriber.canceled.connect(conversation_transcriber_recognition_canceled_cb)
        # stop transcribing on either session stopped or canceled events
        conversation_transcriber.session_stopped.connect(stop_cb)
        conversation_transcriber.canceled.connect(stop_cb)

        try:
            conversation_transcriber.start_transcribing_async()

            # Waits for completion.
            while not transcribing_stop:
                time.sleep(.5)
        finally:
            conversation_transcriber.stop_transcribing_async()

        recognized_text = ' '.join(all_recognized_text)

        # Remove the converted WAV file if the original was an MP3
        if original_audio_file.endswith('.mp3') and os.path.exists(audio_file):
            os.remove(audio_file)
            self.logger.info(f"Removed temporary WAV file: {audio_file}")
 
        return recognized_text
