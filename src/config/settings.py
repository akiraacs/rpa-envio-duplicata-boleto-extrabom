from pydantic_settings import BaseSettings

from src.environment.caminhos_settings import CaminhosSettings
from src.environment.consinco_settings import ConsincoSettings
from src.environment.email_settings import EmailSettings
from src.environment.processo_settings import ProcessoSettings


class Settings(BaseSettings):
    """Configurações do robô."""
    consinco: ConsincoSettings = ConsincoSettings()
    processo: ProcessoSettings = ProcessoSettings()
    email: EmailSettings = EmailSettings()
    caminho: CaminhosSettings = CaminhosSettings()

    class Config:
        env_file = ".env"
        hide_input_in_errors = True
        extra = "ignore"

settings = Settings()
