import json
import azure.cognitiveservices.speech as speechsdk
import speech2text
import data_process as dp
import feature_extract as fe
import model as model
import send_notifications as send

def main():
    web_url = "https://discord.com/api/webhooks/1222689655980294185/LU1I3hZfF5f0SB29D-FUoi8Ny1eMtubwzK0fmr5Z5wWUmDRa-xJdIWIrYzFHDYxW--4a"
    message = "#NOTICE\nPatient#001: Observed speech repetition indicative of potential dementia."
    try:
        # Process audio and get transcription
        transcription = speech2text.speech2text()
        
        # Process the string and extract features (Modify this part based on actual usage)
        file = 'output.json'
        features = dp.process_string(file)
        tag_info = fe.get_tag_info(features)
        
        # Train the model or make predictions based on the features
        prediction = model.train(tag_info)[0]
        
        # If prediction indicates an alert, send a Discord notification
        if prediction == 1:
            send.send_discord_notification(web_url, message)
            result = {"result": transcription, "alert": message}
        else:
            # If prediction is not 1, return a JSON response indicating no alert was triggered
            result = {"result": transcription, "alert": "No alert triggered"}
    except Exception as e:
        result = {"error": str(e)}
    return result

if __name__ == "__main__":
    result = main()
    # print(json.dumps(result, indent=4))

