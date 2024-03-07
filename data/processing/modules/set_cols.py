from typing import Literal


def set_cand_cols(mode: Literal["input", "output"], headers: list = None) -> list:
    if mode == "input":
        cols = [
            "CAND_ID",
            "CAND_NAME",
            "CAND_PTY_AFFILIATION",
            "CAND_ELECTION_YR",
            "CAND_OFFICE_ST",
            "CAND_OFFICE",
            "CAND_OFFICE_DISTRICT",
            "CAND_ICI",
            "CAND_STATUS"
        ]
        indexes = [headers.index(c) for c in cols]
        return indexes
    elif mode == "output":
        cols = [
            "CAND_ID",
            "FEC_NAME",
            "PARTY",
            "YEAR",
            "STATE",
            "OFFICE",
            "DISTRICT",
            "ICI"
        ]
        return cols
    

def set_cmte_cols(mode: Literal["input", "output"], headers: list = None) -> list:
    cols = ["CAND_ID", "CMTE_ID"]
    if mode == "input":
        indexes = [headers.index(c) for c in cols]
        return indexes
    elif mode == "output":
        return cols


def set_cont_cols(mode: Literal["input", "output"], type: Literal["indiv", "oth", "pas2"] = None, headers: list = None) -> list:
    if mode == "input":
        if type != "pas2":
            cols = [
                "CMTE_ID",
                "ENTITY_TP",
                "CITY",
                "STATE",
                "ZIP_CODE",
                "TRANSACTION_AMT",
                "TRANSACTION_DT"
            ]
        else:
            cols = [
                "CAND_ID",
                "ENTITY_TP",
                "CITY",
                "STATE",
                "ZIP_CODE",
                "TRANSACTION_AMT",
                "TRANSACTION_DT"
            ]
        indexes = [headers.index(c) for c in cols]
        return indexes
    elif mode == "output":
        cols = [
            "CAND_ID",
            "ENTITY",
            "CITY",
            "STATE",
            "LOCATION",
            "AMT",
            "DATE",
        ]
        return cols
