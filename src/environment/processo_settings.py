from datetime import datetime

from pydantic import field_validator
from pydantic_settings import BaseSettings

from src.utils import tratamento_datas


class ProcessoSettings(BaseSettings):
    """Variáveis de ambiente relacionadas ao Consinco."""
    data_emissao_filtro: str = tratamento_datas.calcular_data(dias=1, direcao=tratamento_datas.DirecaoCalculo.ANTERIOR)


    @field_validator("data_emissao_filtro", mode="before")
    @classmethod
    def validar_data(cls, v: str) -> str:
        if not v:
            return cls.model_fields["data_emissao_filtro"].default
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"data_emissao_filtro deve estar no formato dd/mm/aaaa, recebido: '{v}'")
        return v


    class Config:
        env_file = ".env"
        hide_input_in_errors = True
        env_prefix = "PROCESSO_"
        extra = "ignore"
