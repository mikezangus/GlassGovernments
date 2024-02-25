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
            "CAND_STATUS",
            "CAND_PCC"
        ]
        indexes = [headers.index(c) for c in cols]
        return indexes
    elif mode == "output":
        cols = [
            "CAND_ID",
            "NAME",
            "PARTY",
            "ELECTION_YEAR",
            "STATE",
            "OFFICE",
            "DISTRICT",
            "ICI",
            "CMTE_ID"
        ]
        return cols


def set_cont_cols(mode: Literal["input", "output"], headers: list = None) -> list:
    if mode == "input":
        cols = [
            "CMTE_ID",
            "ENTITY_TP",
            "CITY",
            "STATE",
            "ZIP_CODE",
            "TRANSACTION_AMT",
            "TRANSACTION_DT",
            "TRAN_ID"
        ]
        indexes = [headers.index(c) for c in cols]
        return indexes
    elif mode == "output":
        cols = [
            "CMTE_ID",
            "CAND_ID",
            "DATE",
            "ENTITY",
            "CITY",
            "STATE",
            "LOCATION",
            "AMT",
            "TRAN_ID"
        ]
        return cols
