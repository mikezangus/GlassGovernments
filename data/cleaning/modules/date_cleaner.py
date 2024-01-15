import pandas as pd


def clean_date(data: object):
    data["contribution_date"] = pd.to_datetime(data["contribution_date"]).dt.date
    return data