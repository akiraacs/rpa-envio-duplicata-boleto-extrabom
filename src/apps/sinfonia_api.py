from http import HTTPStatus

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed

from src.config.settings import settings
from src.models.sinfonia_payload import SinfoniaBotParams, SinfoniaPayload


class SinfoniaApi:
    def __init__(self, data_tratativa: str):
        self.base_url = f"{settings.sinfonia.base_url}"
        self.headers = {
            "Content-Type": "application/json",
            "token": f"{settings.sinfonia.token_api_master}",
        }

        self.data_tratativa = data_tratativa


    def _set_payload(self) -> dict:
        try:
            return SinfoniaPayload(
                bot_name="bot-envio-boleto",
                bot_params=self._set_bot_params(),
                label="api"
            ).model_dump()

        except Exception as e:
            raise httpx.RequestError(f"Erro ao definir payload: {e}")


    def _set_bot_params(self) -> str:
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