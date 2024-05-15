import pandas as pd
from enum import Enum

class CSVType(Enum):
    NUBANK = "nubank"
    INTER = "inter"


def detect_csv_type(csv_lines):
    retorno = CSVType.NUBANK
    for line in csv_lines:
        if "Data Lançamento" in line:
            retorno = CSVType.INTER
            break
    return retorno
