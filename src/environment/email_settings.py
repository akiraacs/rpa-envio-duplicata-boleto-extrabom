from pydantic import field_validator
from pydantic_settings import BaseSettings


class EmailSettings(BaseSettings):
    """Variáveis de ambiente relacionadas ao envio de e-mails."""
    enviar_email: bool = False 
    destinatarios: str | list = ["daniel.ayres@grupocoutinho.com"]

    # Configurações SMTP
    smtp_from: str
    smtp_serv: str
    smtp_port: int
    smtp_user: str
    smtp_pswd: str


    @field_validator("enviar_email", "destinatarios", mode="before")
    @classmethod
    def usar_default_se_vazio(cls, v, info):
        if not v:
            return cls.model_fields[info.field_name].default
        return v


    class Config:
        env_file = ".env"
        extra = "ignore"
        hide_input_in_errors = True
