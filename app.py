from flask import Flask, render_template, url_for, jsonify, request
import towav
import azure.cognitiveservices.speech as speechsdk
import speech2text
import data_process as dp
import feature_extract as fe
import model as model
import send_notifications as send
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/base64_convert')
#def base64_convert():
    #towav.process_audio()

@app.route('/convert_once')
def convert_to_text_once():
    #process audio
    towav.process_audio()
    speech_key, service_region = "328d4b7e54bb445bbff9218e43468a73", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.AudioConfig(filename="temp.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once_async().get()
    return result.text

@app.route('/convert_continuous')
def convert_to_text_continuous():
    web_url = "https://discord.com/api/webhooks/1222689655980294185/LU1I3hZfF5f0SB29D-FUoi8Ny1eMtubwzK0fmr5Z5wWUmDRa-xJdIWIrYzFHDYxW--4a"
    message = "Observed speech repetition indicative of potential dementia."
    try:
        # Process audio and get transcription
        transcription = speech2text.speech2text()
        
        # Process the string and extract features (Modify this part based on actual usage)
        features = dp.process_string(transcription)
        tag_info = fe.get_tag_info(features)
        
        # Train the model or make predictions based on the features
        prediction = model.train(tag_info)[0]
        
        # If prediction indicates an alert, send a Discord notification
        if prediction == 1:
            send.send_discord_notification(web_url, message)
            return jsonify({"result": transcription, "alert": message}), 200
        else:
            # If prediction is not 1, return a JSON response indicating no alert was triggered
            return jsonify({"result": transcription, "alert": "No alert triggered"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500