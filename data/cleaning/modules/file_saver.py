import os


def save_file(data: object, subject, year: str, chamber: str, state: str, input_file_name: str, output_files_dir: str, district: str):
    output_file_name = input_file_name.replace("raw", "cleaned")
    if chamber.lower() == "house":
        output_file_dir = os.path.join(output_files_dir, year, chamber.lower(), state, district)
        os.makedirs(output_file_dir, exist_ok = True)
        output_file_path = os.path.join(output_file_dir, output_file_name)
    elif chamber.lower() == "senate":
        output_file_dir = os.path.join(output_files_dir, year, chamber.lower(), state)
        os.makedirs(output_file_dir, exist_ok = True)
        output_file_path = os.path.join(output_file_dir, output_file_name)
    output_file = data
    output_file.to_csv(output_file_path, index = False)
    print(f"{subject} | Saved cleaned file to:\n{output_file_path}\n")