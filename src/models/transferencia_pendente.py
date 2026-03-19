from pydantic import BaseModel


class TransferenciaPendenteArquivo(BaseModel):
    caixa_origem: str
    data_lancamento: str
    total_lancamento: float = 0.0


class TransferenciaPendenteTabela(BaseModel):
    linha: int
    caixa_origem: str
    caixa_destino: str
    data_lancamento: str
    documento: str
    serie: str
    valor: float = 0.0
    valor_aceito: float = 0.0
    historico: str
