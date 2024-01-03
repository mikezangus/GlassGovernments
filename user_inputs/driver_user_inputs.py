import os
import sys

from .workflows_user_inputs import determine_workflow

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import raw_data_dir


def get_user_inputs(action, source: str):
    output_list = determine_workflow(action, source, raw_data_dir)
    return output_list