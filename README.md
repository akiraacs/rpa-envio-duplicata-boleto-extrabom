# Agendamento de Envio de Duplicatas Boleto

## Descrição
O processo de agendamento de boletos consiste em acessar o ERP Consinco, no módulo de Boletos, filtrar os boletos que necessitam de agendamento e confirmar o agendamento para que seja realizado o envio automático dos e-mails aos fornecedores. Esse procedimento assegura o cumprimento dos prazos e a correta comunicação com os fornecedores.

## Instalação
1. **Pré-requisitos**:
   - Python >= 3.13
   - Instalar dependências:
     ```bash
     python -m venv .venv
     .venv\Script\activate
     pip install -r requirements.txt
     ```

2. **Configuração de variáveis de ambiente**:
   - Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env.example` substituindo os valores de exemplos.

## Execução
1. **Via terminal**:
   ```bash
   python main.py
   ```

## Contato
Dúvidas ou sugestões: contato@27devs.com
