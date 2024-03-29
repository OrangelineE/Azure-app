from data_process import process_string

# Path to your test transcript JSON file
test_file_path = 'testfile.json'

def test():
    results = process_string(test_file_path)
    print(results)

if __name__ == "__main__":
    test()
