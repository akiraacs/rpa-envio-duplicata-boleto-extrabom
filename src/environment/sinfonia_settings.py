from pydantic_settings import BaseSettings


class SinfoniaSettings(BaseSettings):
    """Variáveis de ambiente relacionadas ao Sinfonia."""
    base_url: str = "https://sinfonia.live/api"
    token_api_master: str

    class Config:
        env_file = ".env"
        hide_input_in_errors = True
        env_prefix = "SINFONIA_"
        extra = "ignore"
