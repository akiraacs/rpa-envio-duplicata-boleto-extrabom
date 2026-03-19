from loguru import logger

import src.config.logger
from src.apps.consinco_operador_desktop import ConsincoOperadorDesktop
from src.config.settings import settings
from src.packages.email import Email
from src.utils.comandos_cmd import executar_cmds_manter_sessao_ativa, fechar_sistemas_legados
from src.utils.tratamento_arquivos import limpar_pasta, criar_pastas_essencias_caso_inexistente


def main() -> None:
    """Funcao principal"""
    try:
        nome_rpa = "Envio de Duplicata de Boleto"
        logger.info(f"Iniciando robô - {nome_rpa}")
        execucao_com_erro = False
        msg_data_tratativa = ""
        app_consinco_operador:ConsincoOperadorDesktop = None
        msg_erro = ""

        # executar_cmds_manter_sessao_ativa()
        # fechar_sistemas_legados()
        # criar_pastas_essencias_caso_inexistente()
        # limpar_pasta(caminho_pasta=settings.caminho.pasta_temp)

        msg_data_tratativa = f"Data considerada para consulta/tratativa: {settings.processo.data_conciliacao}"
        logger.info(msg_data_tratativa)

        app_consinco_operador = ConsincoOperadorDesktop(exe_path=settings.caminho.exe_erp_modulo_operador)
        app_consinco_operador.acessar_tela_emissao_duplicatas_boletos()
        app_consinco_operador.filtrar_todos_titulos_por_data(data_consulta=settings.processo.data_conciliacao)

        logger.success(f"Processo {nome_rpa} executado com sucesso")

    except Exception as error:
        msg_erro = str(error)
        execucao_com_erro = True
        logger.error(f"Erro na execução do robô {nome_rpa}.\nErro: {error}")


    finally:
        app_consinco_operador.fechar_sistema() if app_consinco_operador else None

        assunto_email = f"Resultado da execução do RPA - {nome_rpa}"
        corpo_email = str(
            "Resultado da execução do RPA\n"
            f"{msg_data_tratativa}\n\n\n"
        )

        if execucao_com_erro:
            assunto_email += " - ERRO"
            corpo_email += str(
                "\n\n\n"
                "Houve um erro durante a execução do robô:\n"
                f"{msg_erro}\n\n"
                "Por favor, verifique os logs para mais detalhes."
            )
        else:
            assunto_email += " - SUCESSO"

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

        logger.info("Finalizando processo...")

        if execucao_com_erro:
            raise Exception(msg_erro)

if __name__ == "__main__":
    main()