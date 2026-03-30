from loguru import logger

from src.apps.sinfonia_api import SinfoniaApi
from src.config.settings import settings
from src.utils.tratamento_datas import obter_datas_execucao


def acionar_nova_execucao_casos_de_erro() -> None:
    datas_execucao = obter_datas_execucao(arquivo=settings.caminho.arquivo_datas_execucao)
    if datas_execucao:
        for data_exec, tentativa_exec in datas_execucao.items():
            if tentativa_exec != "ok" and tentativa_exec < 2:
                logger.info(f"Iniciando nova execução do sinfonia: {data_exec}")
                sinfonia_api = SinfoniaApi(data_tratativa=data_exec)
                sinfonia_api.acionar_nova_execucao()
                break # Deve fazer uma execucao por vez