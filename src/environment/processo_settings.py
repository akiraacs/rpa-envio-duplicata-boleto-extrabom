from datetime import datetime

from pydantic import field_validator
from pydantic_settings import BaseSettings

from src.utils import tratamento_datas


class ProcessoSettings(BaseSettings):
    """Variáveis de ambiente relacionadas ao Consinco."""
    data_conciliacao: str = tratamento_datas.calcular_data(dias=1, direcao=tratamento_datas.DirecaoCalculo.ANTERIOR)
    usuario_permissao_caixa: str = "MARILIAPR"


    @field_validator("data_conciliacao", mode="before")
    @classmethod
    def validar_data(cls, v: str) -> str:
        if not v:
            return cls.model_fields["data_conciliacao"].default
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"data_conciliacao deve estar no formato dd/mm/aaaa, recebido: '{v}'")
        return v

    @field_validator("usuario_permissao_caixa", mode="before")
    @classmethod
    def usar_default_se_vazio(cls, v):
        if not v:
            return cls.model_fields["usuario_permissao_caixa"].default
        return v


    class Config:
        env_file = ".env"
        hide_input_in_errors = True
        env_prefix = "PROCESSO_"
        extra = "ignore"
