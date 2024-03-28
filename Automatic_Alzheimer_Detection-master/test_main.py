# test_main.py
import data_process as dp
import feature_extract as fe
import model
import send_notifications as send

def main(file):
    x = dp.process_string(file)
    ft = fe.get_tag_info(x)
    pr = model.train(ft)[0]
    if pr == 1:
        send.send_discord_notification("https://discord.com/api/webhooks/1222689655980294185/LU1I3hZfF5f0SB29D-FUoi8Ny1eMtubwzK0fmr5Z5wWUmDRa-xJdIWIrYzFHDYxW--4a", "Speech repetition detected! Potential Alzheimer warning!")
        return True
    return False

if __name__ == "__main__":
    test_file = 'testfile.json'  # Replace with the path to your test file
    result = main(test_file)
    print(f"The result for the file '{test_file}' is: {result}")
