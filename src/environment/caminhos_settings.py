import os

from pydantic import field_validator
from pydantic_settings import BaseSettings


class CaminhosSettings(BaseSettings):
    """Variáveis de ambiente relacionadas a Diretórios."""
    planilha_caixas_rm: str = "resources/xlsx/caixas_rm.xlsx"
    exe_erp_modulo_supervisor: str = r"C:\C5Client\Financeiro\Supervisor.exe"
    exe_erp_modulo_operador: str = r"C:\C5Client\Financeiro\Operador.exe"
    pasta_temp: str = os.path.join(os.getcwd(), "temp")
    arquivo_transferencias_pendentes: str = os.path.join(pasta_temp, "transferencias_pendentes.csv")
    img_tabela_transferencias_pendentes: str = os.path.join(pasta_temp, "tabela_transferencias_pendentes.png")


    @field_validator("planilha_caixas_rm", mode="before")
    @classmethod
    def usar_default_se_vazio(cls, v, info):
        if not v:
            return cls.model_fields[info.field_name].default
        return v


    class Config:
        env_file = ".env"
        hide_input_in_errors = True
        env_prefix = "CAMINHO_"
        extra = "ignore"
