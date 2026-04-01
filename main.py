from loguru import logger

import src.config.logger
from src.apps.consinco_operador_desktop import ConsincoOperadorDesktop
from src.config.settings import settings
from src.packages.email import Email
from src.tasks.acionar_nova_execucao_casos_de_erro import \
    acionar_nova_execucao_casos_de_erro
from src.utils.comandos_cmd import (executar_cmds_pre_execucao,
                                    fechar_sistemas_legados)
from src.utils.tratamento_datas import (obter_datas_execucao,
                                        salvar_datas_execucao)


def main() -> None:
    """Funcao principal"""
    try:
        nome_rpa = "Envio de Duplicatas/Boletos"
        logger.info(f"Iniciando robô - {nome_rpa}")
        execucao_com_erro = False
        app_consinco_operador: ConsincoOperadorDesktop = None
        msg_erro = ""
        msg_data_tratativa = f"Data considerada para consulta/tratativa: {settings.processo.data_emissao_filtro}"
        datas_execucao = obter_datas_execucao(arquivo=settings.caminho.arquivo_datas_execucao)
        logger.info(msg_data_tratativa)

        # Inicializa variaveis para envio de e-mail
        assunto_email = f"Resultado da execução do RPA - {nome_rpa}"
        corpo_email = str(
            "Resultado da execução do RPA\n"
            f"{msg_data_tratativa}\n\n\n"
        )

        executar_cmds_pre_execucao()
        fechar_sistemas_legados()

        app_consinco_operador = ConsincoOperadorDesktop(exe_path=settings.caminho.exe_erp_modulo_operador)
        app_consinco_operador.acessar_tela_emissao_duplicatas_boletos()
        app_consinco_operador.consultar_titulos(data_consulta=settings.processo.data_emissao_filtro)
        status_agendamento, msg_retorno = app_consinco_operador.agendar_envio_email_titulos(data_consulta=settings.processo.data_emissao_filtro)

        if status_agendamento:
            assunto_email += " - SUCESSO"
            corpo_email += f"{msg_retorno}\n"
            logger.success(msg_retorno)
        else:
            assunto_email += " - ATENÇÃO"
            corpo_email += f"{msg_retorno}\n"
            logger.warning(msg_retorno)

        # Adiciona a data de execução atual no arquivo datas de execuções
        datas_execucao[settings.processo.data_emissao_filtro] = "ok"
        salvar_datas_execucao(arquivo=settings.caminho.arquivo_datas_execucao, datas_execucao=datas_execucao)

        logger.success(f"Processo {nome_rpa} executado com sucesso")

    except Exception as error:
        msg_erro = str(error)
        assunto_email += " - ERRO"
        corpo_email += f"{msg_erro}\n\n"

        # Incrementa o número de tentativa de execução para a data de tratativa atual
        tentativa_data_execucao_atual = datas_execucao.get(settings.processo.data_emissao_filtro, None)
        if not tentativa_data_execucao_atual:
            datas_execucao[settings.processo.data_emissao_filtro] = 1
        else:
            datas_execucao[settings.processo.data_emissao_filtro] += 1
        salvar_datas_execucao(arquivo=settings.caminho.arquivo_datas_execucao, datas_execucao=datas_execucao)

        execucao_com_erro = True
        logger.error(f"Erro na execução do robô {nome_rpa}.\nErro: {error}")

    finally:
        app_consinco_operador.fechar_sistema() if app_consinco_operador else None

        if settings.email.enviar_email:
            try:
                email = Email(
                    origem=settings.email.smtp_from,
                    destinatarios=settings.email.destinatarios,
                    assunto=assunto_email,
                    corpo=corpo_email + "\n\n\n",
                )
                email.enviar_email()
            except Exception as error_email:
                logger.error(f"Erro ao enviar e-mail de status: {error_email}")

        acionar_nova_execucao_casos_de_erro()

        logger.info("Finalizando processo...")

        if execucao_com_erro:
            raise Exception(msg_erro)

if __name__ == "__main__":
    main()