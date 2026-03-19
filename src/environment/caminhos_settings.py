from pydantic_settings import BaseSettings


class CaminhosSettings(BaseSettings):
    """Variáveis de ambiente relacionadas a Diretórios."""
    exe_erp_modulo_operador: str = r"C:\C5Client\Financeiro\Operador.exe"

    class Config:
        env_file = ".env"
        hide_input_in_errors = True
        env_prefix = "CAMINHO_"
        extra = "ignore"
