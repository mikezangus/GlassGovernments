import os


def save_cleaned_file(data, subject, year: str, chamber: str, state: str, raw_file_name: str, cleaned_data_dir: str, district: str):
    cleaned_file_name = raw_file_name.replace("raw", "cleanx")
    if chamber.lower() == "house":
        cleaned_file_dir = os.path.join(cleaned_data_dir, year, chamber.lower(), state, district)
        os.makedirs(cleaned_file_dir, exist_ok = True)
        cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
    elif chamber.lower() == "senate":
        cleaned_file_dir = os.path.join(cleaned_data_dir, year, chamber.lower(), state)
        os.makedirs(cleaned_file_dir, exist_ok = True)
        cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
    cleaned_file = data
    cleaned_file.to_csv(cleaned_file_path, index = False)
    print(f"{subject} | Saved cleaned file to:\n{cleaned_file_path}")