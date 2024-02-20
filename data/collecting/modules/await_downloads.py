import os


def await_downloads(dir: str) -> bool:
    try:
        downloads_complete = False
        while not downloads_complete:
            downloads_complete = True
            for file_name in os.listdir(dir):
                if file_name.endswith(".part"):
                    downloads_complete = False
                    break
        print("\nFinished downloading all files")
        return True
    except Exception as e:
        print("Await Downloads | Error:", e)
        return False
