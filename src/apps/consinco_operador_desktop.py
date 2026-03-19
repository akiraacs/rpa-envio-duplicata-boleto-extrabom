import contextlib
import os
import time
from typing import Optional

import pyautogui
import pyscreeze
import pywinauto
from loguru import logger
from pywinauto.application import Application
from tenacity import retry, stop_after_attempt, wait_fixed

from src.config.settings import settings
from src.models.lancamento_conta_corrente import LancamentoContaCorrente

JANELA_OPERADOR_PRINCIPAL = ".*Operador Financeiro*"
JANELA_EMISSAO_DUPLICATAS_BOLETOS = ".*Emissão de Duplicatas/Boletos*"

class ConsincoOperadorDesktop:
    """Classe para interagir com o Consinco - Módulo Operador."""
    def __init__(self, exe_path: str):
        """Inicializa a classe com o caminho do executável do Consinco Operador.

        Args:
            exe_path (str): Caminho completo do executável do Consinco Operador.
        """
        self.exe_path = exe_path
        self.timeout = 60

        if not os.path.exists(self.exe_path):
            raise FileNotFoundError(f"Executável da aplicação não encontrado: {self.exe_path}")

        self.janela_principal: Optional[pywinauto.WindowSpecification] = None
        self.janela_emissao_duplicatas_boletos: Optional[pywinauto.WindowSpecification] = None
        self.app_principal: Application = self._logar()


    def _fechar_janelas_internas(self) -> None:
        """Método utilitario para fechar janelas filhas que possam estar abertas dentro da janela principal do Operador."""
        try:
            janelas_filhas = self.janela_principal.descendants(control_type="Window")

            for j in janelas_filhas:
                j.close()
            logger.info("Todas as janelas internas foram encerradas.")

        except Exception as error:
            raise Exception(f"Erro ao encerrar janelas internas | error: {error}")


    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    def _logar(self) -> Application:
        """Inicia o processo e realiza login com tratamento de tentativas."""
        try:
            logger.info("Iniciando nova sessão do ERP Consinco Operador ...")
            app = Application(backend="uia").start(self.exe_path, timeout=self.timeout)
            time.sleep(2)

            janela_login = app.top_window()
            janela_login.set_focus()

            login = janela_login["UsuárioEdit"]
            # login = janela_login.child_window(title="Boas-vindas", control_type="Edit") # 2 Opção para caso de erro
            login.click_input()
            login.type_keys("^a{BACKSPACE}")
            login.type_keys(settings.consinco.login)

            senha = janela_login.child_window(title="Senha", control_type="Edit")
            senha.click_input()
            senha.type_keys("^a{BACKSPACE}")
            senha.type_keys(settings.consinco.senha)

            janela_login.child_window(title="Entrar", control_type="Button").click()

            if not app.window(title_re=JANELA_OPERADOR_PRINCIPAL).exists(timeout=self.timeout):
                raise Exception(f"Não foi possível se conectar a janela '{JANELA_OPERADOR_PRINCIPAL}'")

            self.janela_principal = app.window(title_re=JANELA_OPERADOR_PRINCIPAL)
            logger.info("Login realizado com sucesso")

            return app

        except Exception as error:
            msg_error = f"Erro durante o processo de login: {error}"
            logger.error(msg_error)
            with contextlib.suppress(Exception):
                app.kill()
            raise Exception(msg_error)


    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def acessar_tela_emissao_duplicatas_boletos(self) -> None:
        """Abre a tela de lançamentos do conta corrente utilizando atalhos de teclado."""
        try:
            self.janela_principal.set_focus()

            pyautogui.moveTo(1, 1)
            time.sleep(0.1)

            # Alt (pressiona e solta) + T para abrir o menu "Transações"
            self.janela_principal.type_keys("%{R}")
            time.sleep(0.3)
            self.janela_principal.type_keys("{DOWN 15}", pause=0.3)
            time.sleep(0.5)
            self.janela_principal.type_keys("{ENTER}")
            time.sleep(1)

            try:
                janela_emissao_duplicatas_boletos = self.janela_principal.window(title_re=JANELA_EMISSAO_DUPLICATAS_BOLETOS, control_type="Window")
                janela_emissao_duplicatas_boletos.wait("exists visible", timeout=5)
            except TimeoutError as error:
                raise TimeoutError()

            self.janela_emissao_duplicatas_boletos = janela_emissao_duplicatas_boletos
            logger.info("Tela de emissão de duplicatas/boletos acessada com sucesso")

        except Exception as error:
            msg_error = f"Erro ao acessar tela de emissão de duplicatas/boletos: {error}"
            logger.error(msg_error)

            self._fechar_janelas_internas()
            raise Exception(msg_error)


    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def filtrar_todos_titulos_por_data(self, data_consulta: str) -> tuple[bool, str]:
        """Define os filtros para a consulta de titulos por data e tipo 'Todos'."""
        try:
            self.janela_principal.set_focus()
            self.janela_emissao_duplicatas_boletos.set_focus()

            btn_boleto_tipo_emissao = self.janela_emissao_duplicatas_boletos.child_window(title="Boleto", control_type="Button")
            btn_boleto_tipo_emissao.click()
            time.sleep(0.2)
            logger.info('Selecionado "Tipo de Emissão" como "Boleto"')

            # data_emissao_de = self.janela_emissao_duplicatas_boletos.child_window(auto_id="4144", control_type="Edit") #por id, nao tao confiavel
            data_emissao_de = self.janela_principal["Data EmissãoEdit"]
            data_emissao_de.set_edit_text(data_consulta)
            time.sleep(0.2)
            logger.info(f"Definido data emissão de: {data_consulta}")

            # data_emissao_ate = self.janela_emissao_duplicatas_boletos.child_window(auto_id="4145", control_type="Edit") #por id, nao tao confiavel
            data_emissao_ate = self.janela_principal["atéEdit4"]
            data_emissao_ate.set_edit_text(data_consulta)
            time.sleep(1)
            logger.info(f"Definido data emissão até: {data_consulta}")

            # combobox_especie = self.janela_emissao_duplicatas_boletos.child_window(auto_id="4139", control_type="ComboBox") #por id, nao tao confiavel
            combobox_especie = self.janela_principal["EspécieComboBox"]
            combobox_especie.click_input()
            combobox_especie.select('BOLETO')
            time.sleep(0.2)
            logger.info('Selecionado "BOLETO" na ComboBox Espécie')

            self.janela_emissao_duplicatas_boletos.set_focus()
            btn_buscar_todos = self.janela_emissao_duplicatas_boletos.child_window(title="Todas(os)", control_type="Button")
            btn_buscar_todos.click_input()
            logger.info('Selecionado "Todas(os)" na opção Buscar Duplicatas/Boletos')
            time.sleep(0.2)

            self.janela_emissao_duplicatas_boletos.set_focus()
            time.sleep(0.2)
            self.janela_principal["Button28"].click_input()

            # Buscar Duplicatas/Boletos
            self.janela_emissao_duplicatas_boletos.set_focus()
            self.janela_emissao_duplicatas_boletos.type_keys("{F8}")
            self.app_principal.wait_cpu_usage_lower(threshold=0.7, timeout=60)
            logger.info("Consultando dados...")
            time.sleep(5)

            # Selecionar todos os títulos
            img_btn_selecionar_todos_titulos = pyscreeze.locateOnScreen("resources/images/btn_selecionar_todos_titulos.png", confidence=0.8)
            if not img_btn_selecionar_todos_titulos:
                raise Exception("Não foi possível localizar por imagem o botão 'Selecionar Todos os Títulos'")
            pyautogui.click(pyautogui.center(img_btn_selecionar_todos_titulos))
            time.sleep(0.5)

            # Enviar boletos por email
            img_btn_enviar_boletos_email = pyscreeze.locateOnScreen("resources/images/btn_enviar_boletos_email.png", confidence=0.8)
            if not img_btn_enviar_boletos_email:
                raise Exception("Não foi possível localizar por imagem o botão 'Enviar Boletos por Email'")
            pyautogui.click(pyautogui.center(img_btn_enviar_boletos_email))
            time.sleep(3)

            self.janela_principal.set_focus()
            time.sleep(0.3)
            popup_atencao = self.janela_principal.child_window(title="Atenção", control_type="Window")
            if not popup_atencao.exists(timeout=5):
                raise Exception('Não foi possível localizar o popup de "Atenção" após clicar no botão "Enviar Boletos por Email"')

            # Verifica se há mensagem de erro ou de sucesso no envio de boletos por e-mail
            msg_popup_atencao = popup_atencao.child_window(control_type="Text", found_index=1).window_text()

            if "Nenhum título selecionado" in msg_popup_atencao:
                return False, f"Não possui titulos disponíveis para a data consultada: {data_consulta}"

            elif "enviar por e-mail os títulos selecionados" in msg_popup_atencao:
                try:
                    popup_atencao.child_window(title="Sim", control_type="Button").click_input()
                except:
                    popup_atencao.child_window(title="Yes", control_type="Button").click_input()
                time.sleep(1)

                popup_aviso_envio_email = self.janela_principal.child_window(title="Aviso", control_type="Window")
                if not popup_aviso_envio_email.exists(timeout=5):
                    raise Exception('Não foi possível localizar o popup de "Aviso" informando que o envio de boletos por e-mail foi agendado com sucesso')

                return True, None

            else:
                raise Exception(
                    f"Não foi possível identificar no popup de Atenção a mensagem que diz se há ou não titulos para enviar por e-mail. \
                    Favor verificar execução ou mensagens mapeadas"
                )

        except Exception as error:
            msg_error = f"Erro ao filtrar lançamentos por data, caixa e tipo 'Todos': {error}"
            logger.error(msg_error)
            raise Exception(msg_error)


    def fechar_sistema(self) -> None:
        """Fecha todos os aplicativos e janelas da aplicação principal do Consinco Operador."""
        self._fechar_janelas_internas()
        if self.app_principal:
            self.app_principal.kill()
            time.sleep(1)
            os.system('taskkill /F /IM operador.exe /FI "USERNAME eq %USERNAME%"')
