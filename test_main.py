# test_main.py
import data_process as dp
import feature_extract as fe
import model
import send_notifications as send

def main():
    # x = dp.process_string(file)
    y = ["Daisy. It's me, Benjamin. Benjamin. Oh my God. Of course it's you. Benjamin.", 0, 0, 0, 0]
    ft = fe.get_tag_info(y)
    pr = model.train(ft)[0]
    if pr == 1:
        send.send_discord_notification("https://discord.com/api/webhooks/1222689655980294185/LU1I3hZfF5f0SB29D-FUoi8Ny1eMtubwzK0fmr5Z5wWUmDRa-xJdIWIrYzFHDYxW--4a", "Observed speech repetition in Patient #001. Possible early dementia sign, advise evaluation.")
        return True
    return False

if __name__ == "__main__":
    test_file = 'output.json'  # Replace with the path to your test file
    result = main()
    print(f"The result is: {result}")
