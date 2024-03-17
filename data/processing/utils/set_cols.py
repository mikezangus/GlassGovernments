from typing import Literal
from .data_types import DataType


COL_MAP: dict[
    str,
    dict[
        str,
        dict[
            str,
            list[str]
        ]
    ]
] = {
    "cand": {
        "input": [
            "CAND_ID",
            "CAND_NAME",
            "CAND_PTY_AFFILIATION",
            "CAND_ELECTION_YR",
            "CAND_OFFICE_ST",
            "CAND_OFFICE",
            "CAND_OFFICE_DISTRICT",
            "CAND_STATUS"
        ],
        "output": [
            "CAND_ID",
            "FEC_NAME",
            "PARTY",
            "YEAR",
            "STATE",
            "OFFICE",
            "DISTRICT",
        ]
    },
    "cmte": {
        "input": [
            "CAND_ID",
            "CMTE_ID"
        ],
        "output": [
            "CAND_ID",
            "CMTE_ID"
        ]
    },
    "cont": {
        "input": {
            "indiv": [
                "CMTE_ID",
                "ENTITY_TP",
                "CITY",
                "STATE",
                "ZIP_CODE",
                "TRANSACTION_AMT",
                "TRANSACTION_DT"
            ],
            "oth": [
                "CMTE_ID",
                "ENTITY_TP",
                "CITY",
                "STATE",
                "ZIP_CODE",
                "TRANSACTION_AMT",
                "TRANSACTION_DT"
            ],
            "pas2": [
                "CAND_ID",
                "ENTITY_TP",
                "CITY",
                "STATE",
                "ZIP_CODE",
                "TRANSACTION_AMT",
                "TRANSACTION_DT"
            ]
        },
        "output": [
            "CAND_ID",
            "ENTITY",
            "CITY",
            "CONT_STATE",
            "LOCATION",
            "AMT",
            "DATE",
            "DOMESTIC"
        ]
    },
    "dist": {
        "input": [
            "STATEFP",
            "CD118FP",
            "geometry"
        ],
        "output": [
            "STATE",
            "DISTRICT",
            "GEOMETRY"
        ]
    }
    ,
    "name": {
        "output": [
            "CAND_ID",
            "NAME",
            "PARTY",
            "YEAR",
            "STATE",
            "OFFICE",
            "DISTRICT",
        ]
    }
}


def set_cols(
    type: DataType,
    mode: Literal["input", "output"],
    headers: list[str] = None,
    cont_type: Literal["indiv", "oth", "pas2"] = None
) -> list[str]:
    if type not in COL_MAP:
        raise ValueError(
            f"Type {type} is invalid.\nValid types:\n{', '.join(COL_MAP.keys())}"
        )
    cols = COL_MAP[type][mode]
    if type == "cont" and mode == "input":
        if not cont_type or cont_type not in cols:
            raise ValueError(
                f"Contribution type {cont_type} is invalid. Valid types:\n{', '.join(cols.keys())}"
            )
        cols = cols[cont_type]
    if mode == "input":
        if headers is None:
            raise ValueError(
                "To set input columns, headers must be provided"
            )
        return [headers.index(c) for c in cols]
    return cols
