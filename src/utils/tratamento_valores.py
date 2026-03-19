
def converter_valor(valor: str) -> float:
    """Converte o valor para float, considerando o formato de valor do Excel.

    Args:
        valor (str): Valor a ser convertido.

    Returns:
        float: Valor convertido para float.
    """
    valor = valor.strip()
    if "," in valor and "." in valor:
        if valor.index(".") < valor.index(","):
            # Formato: 1.067,00 (BR) → ponto é milhar, vírgula é decimal
            return float(valor.replace(".", "").replace(",", "."))
        else:
            # Formato: 1,067.00 (US) → vírgula é milhar, ponto é decimal
            return float(valor.replace(",", ""))
    elif "," in valor:
        # Só vírgula: 1067,00 → decimal
        return float(valor.replace(",", "."))
    return float(valor)