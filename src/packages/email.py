import ast
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename

from src.config.settings import settings


class Email:
    """Classe para envio de e-mail."""
    def __init__(
        self,
        origem: str,
        destinatarios: list, 
        assunto: str = None, 
        corpo: str = None, 
        arquivos: list = None
    ) -> None:
        """Inicializa a classe de e-mail.
        
        Args:
            origem (str): Endereço de e-mail do remetente.
            destinatarios (list): Lista de destinatários do e-mail.
            assunto (str, optional): Assunto do e-mail. Defaults to None.
            corpo (str, optional): Corpo do e-mail. Defaults to None.
            arquivos (list, optional): Lista de caminhos de arquivos para anexar. Defaults to None.
        """
        if arquivos is None:
            arquivos = []
        if isinstance(destinatarios, str):
            destinatarios = ast.literal_eval(destinatarios)

        self.origem = origem
        self.destinatarios = destinatarios
        self.assunto = assunto
        self.corpo = corpo
        self.arquivos = arquivos


    def __enviar_email_com_smtp(self) -> None:
        """Envia e-mail utilizando SMTP."""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.origem
            msg["To"] = "; ".join(self.destinatarios)
            msg["Date"] = formatdate(localtime=True)
            msg["Subject"] = self.assunto
            msg.attach(MIMEText(self.corpo, "plain"))

            for arquivo in self.arquivos:
                if not os.path.exists(arquivo):
                    raise Exception(f"Erro ao enviar e-mail - SMTP | arquivo não encontrado: {arquivo}")
                
                with open(arquivo, "rb") as file:
                    part = MIMEApplication(file.read(), Name=basename(arquivo))
                    
                part["Content-Disposition"] = 'attachment; filename="%s"' % basename(arquivo)
                msg.attach(part)

            with smtplib.SMTP(host=settings.email.smtp_serv, port=settings.email.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(user=settings.email.smtp_user, password=settings.email.smtp_pswd)
                smtp.sendmail(
                    from_addr=settings.email.smtp_from,
                    to_addrs=self.destinatarios,
                    msg=msg.as_string()
                )
                smtp.close()

        except Exception as error:
            raise Exception(f"Erro ao enviar e-mail - SMTP | erro: {error}")

    def enviar_email(self) -> None:
        """Envia e-mail."""
        self.__enviar_email_com_smtp()