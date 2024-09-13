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
    
    def transcribe(self, audio_file: str):
        self.logger.info(f"Transcribing file: {audio_file}")
        if audio_file.endswith('.mp3'):
            wav_file = audio_file.replace('.mp3', '.wav')
            AudioSegment.from_mp3(audio_file).export(wav_file, format='wav')
            audio_file = wav_file

        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
        recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, language='zh-CN', audio_config=audio_config)
        # recognizer = speechsdk.transcription.ConversationTranscriber(speech_config=self.speech_config, language='zh-CN', audio_config=audio_config)
        
        done = False
        all_recognized_text = []  # List to store all recognized text

        def stop_cb(evt: speechsdk.SessionEventArgs):
            """Callback that signals to stop continuous recognition upon receiving an event `evt`."""
            print(f'CLOSING on {evt}')
            nonlocal done
            done = True

        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            """Callback to handle recognized text."""
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print(f'RECOGNIZED: {evt.result.text}')
                all_recognized_text.append(evt.result.text)
            elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized.")

        # Connect callbacks to the events fired by the speech recognizer
        recognizer.recognized.connect(lambda evt: print(f'RECOGNIZING: {evt.result.text}'))
        recognizer.recognized.connect(recognized_cb)
        recognizer.session_started.connect(lambda evt: print(f'SESSION STARTED: {evt}'))
        recognizer.session_stopped.connect(lambda evt: print(f'SESSION STOPPED {evt}'))
        recognizer.canceled.connect(lambda evt: print(f'CANCELED {evt}'))

        # Stop continuous recognition on either session stopped or canceled events
        recognizer.session_stopped.connect(stop_cb)
        recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        recognizer.start_continuous_recognition()

        while not done:
            time.sleep(.5)

        recognizer.stop_continuous_recognition()

        # Combine all recognized text into a single string
        self.logger.info(f"Transcription complete for {audio_file}")
        self.logger.info(f"Recognized text: {all_recognized_text}")
        return ' '.join(all_recognized_text)
    

    def recognize_from_file(self,  audio_file: str ):
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

        conversation_transcriber.start_transcribing_async()

        # Waits for completion.
        while not transcribing_stop:
            time.sleep(.5)

        conversation_transcriber.stop_transcribing_async()

        return ' '.join(all_recognized_text)
