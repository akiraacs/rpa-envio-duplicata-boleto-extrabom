from pydantic import BaseModel


class SinfoniaBotParams(BaseModel):
    """Parâmetros do bot para requisição no Sinfonia."""
    # Processo
    processo_data_emissao_filtro: str

    # Caminhos
    caminho_exe_erp_modulo_operador: str
    caminho_onedrive_robo: str
    caminho_arquivo_datas_execucao: str

    # E-mail
    enviar_email: str
    destinatarios: str


class SinfoniaPayload(BaseModel):
    """Payload para requisição no Sinfonia."""
    agent_name: str = ""
    bot_name: str = ""
    bot_params: str = ""
    bot_version: str = ""
    label: str = ""
    webhook_url: str = ""
