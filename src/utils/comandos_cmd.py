import os
import socket


def executar_cmds_manter_sessao_ativa() -> None:
    """Executa comandos Shell antes de iniciar a execução do processo"""
    nome_servidor = socket.gethostname().lower()
    if "src-" not in nome_servidor:
        return

    # Keep Session Windows
    os.system('FOR /F "skip=1 tokens=3 usebackq" %X in (`query session %USERNAME%`) DO tscon %X /dest:console')
    # Set Resolution 1920x1080
    os.system("powershell.exe -Command Set-DisplayResolution -Width 1920 -Height 1080 -Force")
    # Set 100% Scale (broke pyautogui != 100%)
    # https://learn.microsoft.com/en-us/answers/questions/3744044/automating-display-scale-percentages
    os.system(f"{os.getcwd()}/resources/exe/SetDpi.exe 100 1")


def fechar_sistemas_legados() -> None:
    """Fecha todos os aplicativos e janelas da aplicação principal do Consinco Supervisor e Operador."""
    os.system('taskkill /F /IM operador.exe /FI "USERNAME eq %USERNAME%"')
    os.system('taskkill /F /IM supervisor.exe /FI "USERNAME eq %USERNAME%"')
