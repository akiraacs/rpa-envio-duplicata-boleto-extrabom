from pydantic import field_validator
from pydantic_settings import BaseSettings


class CaminhosSettings(BaseSettings):
    """Variáveis de ambiente relacionadas a Diretórios."""
    exe_erp_modulo_operador: str = r"C:\C5Client\Financeiro\Operador.exe"
    onedrive_robo: str = r"C:\Users\robo\OneDrive - Extrabom Supermercados\RPA-PYTHON\bot-envio-duplicata-boleto"
    arquivo_datas_exec_sucesso: str = f"{onedrive_robo}\datas_exec_sucesso.json"


    @field_validator("arquivo_datas_exec_sucesso", mode="before")
    @classmethod
    def validar_arquivo(cls, v: str) -> str:
        if not v:
            return cls.model_fields["arquivo_datas_exec_sucesso"].default
        return v

    class Config:
        env_file = ".env"
        hide_input_in_errors = True
        env_prefix = "CAMINHO_"
        extra = "ignore"
