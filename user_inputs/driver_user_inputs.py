import os
import sys

from workflows_user_inputs import determine_workflow

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import raw_data_dir


# def get_user_inputs(action: str, source: str, raw_data_dir: str):
determine_workflow("test", "files", raw_data_dir)