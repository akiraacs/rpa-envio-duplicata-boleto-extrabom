import ctypes
import os
import socket

import pyautogui
import win32api
import win32con
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed


def executar_cmds_pre_execucao() -> None:
    """Prepara o ambiente de Produção para garantir a execução da interface gráfica.

    Este método realiza a manutenção da sessão de consola, garantindo que o 
    Windows mantenha a GUI ativa após o logoff do RDP, e padroniza a 
    resolução e escala (DPI) para assegurar a precisão dos cliques e 
    do reconhecimento de imagem.

    Note:
        - Este método só é executado se 'ConfigsGeral.AMBIENTE_PROD' for True.
        - O comando 'tscon' exige privilégios administrativos para redirecionar 
        a sessão com sucesso.

    Returns:
        None
    """
    nome_servidor = socket.gethostname().lower()
    if "src-" not in nome_servidor:
        return

    os.system('FOR /F "skip=1 tokens=3 usebackq" %X in (`query session %USERNAME%`) DO tscon %X /dest:console')
    pyautogui.sleep(3)

    _mudar_resolucao_win32(largura=1920, altura=1080)
    _mudar_dpi_100()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
def _mudar_resolucao_win32(largura: int =1920, altura: int=1080) -> None:
    """Força a alteração da resolução do monitor utilizando a Win32 API e PowerShell.

    Este método ajusta as configurações de PelsWidth e PelsHeight do driver de 
    exibição. Caso a API Win32 não surta efeito, utiliza um comando forçado via 
    PowerShell como plano de contingência.

    Args:
        largura (int): Largura desejada em pixels (padrão 1920).
        altura (int): Altura desejada em pixels (padrão 1080).

    Note:
        O uso de @retry garante que, se o driver de vídeo estiver ocupado 
        ou em transição, o robô tentará novamente antes de falhar.

    Raises:
        Exception: Se, após todas as tentativas e métodos (API e PowerShell), 
            a resolução atual lida pelo PyAutoGUI for diferente da solicitada.
    """
    logger.info(f"Tentando forçar {largura}x{altura} via Win32 API...")
    devmode = ctypes.create_string_buffer(148)
    ctypes.memset(devmode, 0, 148)
    ctypes.memmove(devmode[36:38], b"\x94\x00", 2)
    dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    dm.PelsWidth = largura
    dm.PelsHeight = altura
    dm.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    resultado = win32api.ChangeDisplaySettings(dm, 0)

    largura_atual, altura_atual = pyautogui.size()
    if largura_atual != largura or altura_atual != altura:
        logger.warning(resultado)
        os.system("powershell.exe -Command Set-DisplayResolution -Width 1920 -Height 1080 -Force")
        pyautogui.sleep(5)
        largura_atual, altura_atual = pyautogui.size()
        if largura_atual != largura or altura_atual != altura:
            raise Exception(
                f"Erro ao mudar resolução para {largura}x{altura}, sistema insiste em {largura_atual}x{altura_atual}."
            )

    else:
        logger.success(f"Resolução alterada com sucesso para {largura}x{altura}")
        return

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
def _mudar_dpi_100() -> None:
    """Força a escala (DPI) do Windows para 100% para garantir fidelidade visual.

    Este método executa um utilitário externo para ajustar o DPI e valida a 
    alteração através de chamadas à user32.dll. A escala de 100% é mandatória 
    para que o reconhecimento de imagem (Computer Vision) funcione corretamente.

    Note:
        - O Windows utiliza 96 DPI como valor padrão para a escala de 100%.
        - Depende do executável 'SetDpi.exe' localizado na pasta de recursos.

    Raises:
        Exception: Caso o executável falhe ou se, após a tentativa, o DPI 
            lido pelo sistema ainda for diferente de 96 (100%).
    """
    try:
        porcentagem = 100
        os.system(f'"{os.getcwd()}/resources/exe/SetDpi.exe" 100 1')
        dpi_raw = ctypes.windll.user32.GetDpiForSystem()
        dpi_percent = int((dpi_raw / 96) * porcentagem)
        if dpi_percent != porcentagem:
            raise Exception(f"DPI atual: {dpi_percent}")
        logger.success(f"DPI atual definido com {dpi_percent}%")
    except Exception as error:
        raise Exception(f"Erro ao definir DPI 100% | {str(error)}")


def fechar_sistemas_legados() -> None:
    """Fecha todos os aplicativos e janelas da aplicação principal do Consinco Supervisor e Operador."""
    os.system('taskkill /F /IM operador.exe /FI "USERNAME eq %USERNAME%"')
    os.system('taskkill /F /IM supervisor.exe /FI "USERNAME eq %USERNAME%"')
