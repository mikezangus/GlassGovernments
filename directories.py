import os


current_path = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_path, "data")
downloads_container_dir = os.path.join(data_dir, "downloads_container")
source_data_dir = os.path.join(data_dir, "source")
raw_data_dir = os.path.join(data_dir, "raw")
cleaned_data_dir = os.path.join(data_dir, "cleanx")