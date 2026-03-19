from pydantic import BaseModel


class LancamentoContaCorrente(BaseModel):
    historico: str
    valor: str
