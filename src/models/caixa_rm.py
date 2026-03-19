from pydantic import BaseModel


class CaixaRM(BaseModel):
    nome: str
    numero: str
    vlt_total_lancamentos: str = ""
    msg_status: str = "Não foi possivel definir um status para este caixa. Favor verificar!"

    def __str__(self):
        return str(
            f"Nome: {self.nome}\n"
            f"Número: {self.numero}\n"
            f"Valor total lançamentos: {self.vlt_total_lancamentos}\n"
            f"Status: {self.msg_status}\n\n"
        )