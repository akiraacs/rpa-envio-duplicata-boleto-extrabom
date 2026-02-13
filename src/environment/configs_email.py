import os


class ConfigsEmail:
    """Variáveis de ambiente relacionadas ao envio de e-mails."""
    ENVIAR_EMAIL = os.getenv("SEND_EMAIL", "false")
    ENVIAR_EMAIL = ENVIAR_EMAIL.lower() == "true"

    MAIL_TO = os.getenv("EMAIL_TO", "daniel.ayres@grupocoutinho.com")

    MAIL_FROM = os.getenv("SMTP_FROM")
    if not MAIL_FROM:
        raise ValueError("SMTP_FROM is not set")

    MAIL_SERVER = os.getenv("SMTP_SERV")
    if not MAIL_SERVER:
        raise ValueError("SMTP_SERV is not set")

    MAIL_PORT = os.getenv("SMTP_PORT")
    if not MAIL_PORT:
        raise ValueError("SMTP_PORT is not set")

    MAIL_USER = os.getenv("SMTP_USER")
    if not MAIL_USER:
        raise ValueError("SMTP_USER is not set")

    MAIL_PSWD = os.getenv("SMTP_PSWD")
    if not MAIL_PSWD:
        raise ValueError("SMTP_PSWD is not set")