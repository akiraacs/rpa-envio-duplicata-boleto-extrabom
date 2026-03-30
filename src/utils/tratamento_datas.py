import json
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path


class DirecaoCalculo(Enum):
    ANTERIOR = -1
    POSTERIOR = 1

def calcular_data(
    dias: int,
    direcao: DirecaoCalculo = DirecaoCalculo.ANTERIOR,
    data_referencia: datetime = datetime.now()
) -> str:
    """Calcula uma nova data com base em uma data de referência, um número de dias e uma direção de cálculo.

    Args:
        dias (int): O número de dias a ser adicionado ou subtraído da data de referência.
        direcao (DirecaoCalculo, optional): A direção do cálculo, indicando se os dias devem ser adicionados ou subtraídos. Padrão é DirecaoCalculo.ANTERIOR.
        data_referencia (datetime, optional): A data de referência para o cálculo. Padrão é a data atual.

    Returns:
        datetime: A nova data calculada.
    """
    return (data_referencia + (direcao.value * timedelta(days=dias))).strftime("%d/%m/%Y")


def obter_datas_execucao(arquivo: str) -> list[str]:
    """Lê a lista de datas de execução do arquivo JSON e retorna uma lista de strings.

    Args:
        arquivo (str): Caminho completo do arquivo JSON.

    Returns:
        list[str]: Lista de datas de execução.
    """
    arquivo = Path(arquivo)
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo que armazena datas de execução não encontrado: {arquivo}")

    return json.loads(arquivo.read_text(encoding="utf-8"))


def salvar_datas_execucao(arquivo: str, datas_execucao: list[str]) -> None:
    """Salva a lista de datas de execução no arquivo JSON.

    Args:
        arquivo (str): Caminho completo do arquivo JSON.
        datas_execucao (list[str]): Lista de datas de execução.
    """
    arquivo = Path(arquivo)
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo que armazena datas de execução não encontrado: {arquivo}")

    datas_execucao = _limpar_datas_antigas(datas_execucao)
    datas_execucao = _inicializar_datas_pendentes(datas_execucao)

    arquivo.write_text(json.dumps(datas_execucao, indent=4, ensure_ascii=False), encoding="utf-8")


def _limpar_datas_antigas(datas: list[str]) -> list[str]:
    """Remove datas antigas de uma lista de datas.

    Args:
        datas (list[str]): Lista de datas.

    Returns:
        list[str]: Lista de datas limpa.
    """
    limite = datetime.today() - timedelta(days=30)
    return {d: t for d, t in datas.items() if datetime.strptime(d, "%d/%m/%Y") > limite}


def _inicializar_datas_pendentes(datas: dict[str, int]) -> dict[str, int]:
    datas_referencia = obter_qtd_especifica_datas_passadas(5)
    for data in datas_referencia:
        if data not in datas:
            datas[data] = 0
    return datas


def obter_qtd_especifica_datas_passadas(qtd: int) -> list[str]:
    """Retorna as últimas `qtd` datas passadas a partir de ontem.
    
    Args:
        qtd (int): Quantidade de datas passadas a serem retornadas.
    """
    if qtd <= 0:
        return []
    return [
        (datetime.today() - timedelta(days=i)).strftime("%d/%m/%Y")
        for i in range(1, qtd + 1)
    ]