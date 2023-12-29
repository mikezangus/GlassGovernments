import os


project_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.join(project_dir, "data")
data_cleaning_dir = os.path.join(project_dir, "data_cleaning")
data_collecting_dir = os.path.join(project_dir, "data_collecting")
data_uploading_dir = os.path.join(project_dir, "data_uploading")
us_states_dir = os.path.join(project_dir, "us_states")
user_inputs_dir = os.path.join(project_dir, "user_inputs")

downloads_container_dir = os.path.join(data_dir, "downloads_container")
source_data_dir = os.path.join(data_dir, "source")
raw_data_dir = os.path.join(data_dir, "raw")
cleaned_data_dir = os.path.join(data_dir, "cleanx")