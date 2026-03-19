from pydantic_settings import BaseSettings


class ConsincoSettings(BaseSettings):
    """Variáveis de ambiente relacionadas ao Consinco."""
    login: str
    senha: str

    class Config:
        env_file = ".env"
        hide_input_in_errors = True
        env_prefix = "ERP_CONSINCO_"
        extra = "ignore"
