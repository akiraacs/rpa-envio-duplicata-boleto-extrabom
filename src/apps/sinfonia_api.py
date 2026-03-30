from http import HTTPStatus

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed

from src.config.settings import settings
from src.models.sinfonia_payload import SinfoniaBotParams, SinfoniaPayload


class SinfoniaApi:
    """Classe para interagir com o Sinfonia - Módulo de API."""
    def __init__(self, data_tratativa: str):
        """Inicializa a classe com a data de tratativa do processo.
        
        Args:
            data_tratativa (str): Data de tratativa do processo.
        """
        self.base_url = f"{settings.sinfonia.base_url}"
        self.headers = {
            "Content-Type": "application/json",
            "token": f"{settings.sinfonia.token_api_master}",
        }

        self.data_tratativa = data_tratativa


    def _set_payload(self) -> dict:
        """Define o payload para requisição no Sinfonia."""
        try:
            return SinfoniaPayload(
                bot_name="bot-envio-boleto",
                bot_params=self._set_bot_params(),
                label="api"
            ).model_dump()

        except Exception as e:
            raise httpx.RequestError(f"Erro ao definir payload: {e}")


    def _set_bot_params(self) -> str:
        """Define os parâmetros do bot para requisição no Sinfonia."""
        try:
            return SinfoniaBotParams(
                processo_data_emissao_filtro=str(self.data_tratativa),
                caminho_exe_erp_modulo_operador=str(settings.caminho.exe_erp_modulo_operador),
                caminho_onedrive_robo=str(settings.caminho.onedrive_robo),
                caminho_arquivo_datas_execucao=str(settings.caminho.arquivo_datas_execucao),
                enviar_email=str(settings.email.enviar_email),
                destinatarios=str(settings.email.destinatarios),
            ).model_dump_json()

        except Exception as e:
            raise httpx.RequestError(f"Erro ao definir bot_params para payload: {e}")


    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    def acionar_nova_execucao(self) -> None:
        """Aciona uma nova execução do bot no Sinfonia."""
        try:
            response = httpx.post(
                url=f"{settings.sinfonia.base_url}/v1/run",
                headers=self.headers,
                json=self._set_payload(),
            )

            if not response.status_code == HTTPStatus.OK:
                response.raise_for_status()

        except Exception as e:
            raise httpx.RequestError(f"Erro ao executar nova execução no Sinfonia: {e}")