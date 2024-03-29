import requests
import json

def send_discord_notification(webhook_url, message):
    # Create the JSON payload
    data = {
        "content": message,
        "username": "Notification Bot"
    }

    # POST request to the Discord webhook URL
    response = requests.post(webhook_url, json=data)

    # Check the response
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")
        print(f"Response: {response.text}")
