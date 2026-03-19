from datetime import datetime, timedelta
from enum import Enum


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