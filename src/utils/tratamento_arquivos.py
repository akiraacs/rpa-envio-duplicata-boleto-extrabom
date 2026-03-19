import glob
import os
from pathlib import Path

from loguru import logger


def excluir_arquivo(arquivo: str) -> None:
    arquivo = Path(arquivo)

    if not arquivo.exists():
        logger.warning(f"Arquivo não encontrado: {arquivo}")
        return

    arquivo.unlink()
    logger.success(f"Arquivo excluido: {arquivo}")


def limpar_pasta(caminho_pasta: str) -> None:
    """Remove todos os arquivos da pasta, mantém a pasta vazia"""
    arquivos = glob.glob(os.path.join(caminho_pasta, "*"))

    for arquivo in arquivos:
        if os.path.isfile(arquivo):
            os.remove(arquivo)

    logger.info(f"Todos os arquivos da pasta {caminho_pasta} foram removidos.")


def criar_pastas_essencias_caso_inexistente() -> None:
    """Cria as pastas essencias caso não existam."""
    base = Path(os.getcwd())
    (base / "temp").mkdir(exist_ok=True)
    (base / "logs").mkdir(exist_ok=True)