import towav
import azure.cognitiveservices.speech as speechsdk
import time 
import json

def speech2text():
    #process audio
    towav.process_audio()
    
    """performs continuous speech recognition with input from an audio file"""
    speech_key, service_region = "328d4b7e54bb445bbff9218e43468a73", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.output_format = speechsdk.OutputFormat.Detailed
    audio_config = speechsdk.AudioConfig(filename="temp.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    all_transcripts = []  # This will collect transcript texts
    all_items = []  # This will collect individual words with timings and confidence

    def handle_final_result(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # Parse the detailed results
            json_result = json.loads(evt.result.json)
            best_result = json_result['NBest'][0]
            all_transcripts.append(best_result['Display'])
            for word in best_result['Words']:
                if 'Word' in word:  # Check if 'Word' key exists to avoid key errors
                    item = {
                        "start_time": "{:.3f}".format(word['Offset'] / 10000000) if 'Offset' in word else None,  
                        "end_time": "{:.3f}".format((word['Offset'] + word['Duration']) / 10000000) if 'Offset' in word and 'Duration' in word else None,
                        "alternatives": [
                            {
                                "confidence": word['Confidence'] if 'Confidence' in word else None,
                                "content": word['Word']
                            }
                        ],
                        "type": "pronunciation"
                    }
                all_items.append(item)
    speech_recognizer.recognized.connect(handle_final_result)
    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    results_json = {
        "jobName": "transcribe",
        "accountId": "bunnies",
        "results": {
            "transcripts": [{"transcript": " ".join(all_transcripts)}],
            "items": all_items
        },
        "status": "COMPLETED"
    }

    output_filename = "output.json"
    
    # Write the JSON data to the file
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(results_json, file, ensure_ascii=False, indent=4)
    print(f"Results written to {output_filename}")
    return results_json
