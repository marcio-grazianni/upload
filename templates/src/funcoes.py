from enum import Enum


class CSVType(Enum):
    NUBANK = "nubank"
    INTER = "inter"


def detect_csv_type(csv_lines):
    """
    Detecta o tipo de CSV com base na presença da string "Data Lançamento" nas linhas do CSV.
    
    Parâmetros:
    - csv_lines: Lista de strings representando as linhas do CSV.
    
    Retorna:
    - CSVType: Um valor Enum representando o tipo detectado do CSV.
    """
    retorno = CSVType.NUBANK
    for line in csv_lines:
        if "Data Lançamento" in line:
            retorno = CSVType.INTER
            break
    return retorno


def detect_csv_delimiter(csv_type):
    """
    Detecta o delimitador CSV com base no CSVType fornecido.
    
    Parâmetros:
    - csv_type: Um enum representando o tipo de CSV.
    
    Retorna:
    - str: O delimitador ("," para NUBANK, ";" caso contrário).
    """
    return "," if csv_type == CSVType.NUBANK else ";"
