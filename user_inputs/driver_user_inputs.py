from .workflows_user_inputs import determine_workflow


def get_user_inputs(action, source: str, data_dir: str = None):
    output_list = determine_workflow(action, source, data_dir)
    return output_list