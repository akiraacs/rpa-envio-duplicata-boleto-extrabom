# Agendamento de Envio de Duplicatas/Boletos

## Descricao
RPA para agendamento do envio de duplicatas/boletos por e-mail no ERP Consinco (modulo Operador).

O robo:
- acessa o ERP Consinco no modulo Operador Financeiro;
- navega ate a tela de Emissao de Duplicatas/Boletos;
- filtra os titulos por data de emissao e especie "BOLETO";
- seleciona todos os titulos e agenda o envio por e-mail aos fornecedores;
- registra o resultado da execucao (sucesso, atencao ou erro) em arquivo de controle de datas;
- em caso de erro, aciona automaticamente uma nova execucao via API Sinfonia (ate 2 tentativas por data);
- envia e-mail com o resultado da execucao (sucesso, atencao ou erro).

## Fluxo resumido
1. Executa comandos para manter a sessao RDP ativa e ajustar resolucao/escala da tela.
2. Encerra processos legados do Consinco (Operador/Supervisor).
3. Abre o ERP Consinco no modulo Operador e realiza login.
4. Acessa a tela de Emissao de Duplicatas/Boletos via atalhos de teclado.
5. Define filtros: tipo de emissao "Boleto", data de emissao e especie "BOLETO".
6. Consulta os titulos disponiveis.
7. Seleciona todos os titulos (via reconhecimento de imagem) e agenda o envio por e-mail.
8. Trata janelas de "Atencao" e "Aviso" para confirmar o agendamento.
9. Registra a data de execucao no arquivo de controle (`datas_execucao.json`).
10. Fecha o sistema e envia e-mail de status com o resultado.
11. Verifica execucoes pendentes com erro e aciona nova execucao via API Sinfonia (retry automatico).

## Estrutura principal
```
├── main.py                              # Orquestracao do processo
├── pyproject.toml                       # Configuracoes do projeto e dependencias (uv)
├── uv.lock                             # Lockfile de dependencias (uv)
├── requirements.txt                     # Dependencias (pip)
├── .env.example                         # Exemplo de variaveis de ambiente
├── .python-version                      # Versao do Python (3.13)
├── resources/
│   └── images/                          # Imagens de referencia para automacao (pyautogui)
├── src/
│   ├── apps/
│   │   ├── consinco_operador_desktop.py # Automacao do Operador Financeiro (login, navegacao, consulta e agendamento)
│   │   └── sinfonia_api.py              # Integracao com API Sinfonia (retry de execucoes com erro)
│   ├── config/
│   │   ├── logger.py                    # Configuracao do Loguru (arquivo + stdout)
│   │   └── settings.py                  # Carregamento centralizado das configuracoes (Pydantic Settings)
│   ├── environment/
│   │   ├── caminhos_settings.py         # Caminhos dos executaveis e diretorios (OneDrive, datas_execucao.json)
│   │   ├── consinco_settings.py         # Credenciais do ERP Consinco
│   │   ├── email_settings.py            # Configuracoes de e-mail/SMTP
│   │   ├── processo_settings.py         # Variaveis do processo (data de emissao)
│   │   └── sinfonia_settings.py         # Configuracoes da API Sinfonia (URL base e token)
│   ├── models/
│   │   └── sinfonia_payload.py          # Modelos de dados para payload da API Sinfonia (Pydantic)
│   ├── packages/
│   │   └── email.py                     # Envio SMTP com suporte a anexos
│   ├── tasks/
│   │   └── acionar_nova_execucao_casos_de_erro.py  # Retry automatico via Sinfonia para execucoes com erro
│   └── utils/
│       ├── comandos_cmd.py              # Comandos de sessao RDP e encerramento de processos
│       └── tratamento_datas.py          # Utilitarios de manipulacao de datas e controle de execucoes
└── tests/                               # Testes automatizados
```

## Requisitos
- Windows (automacao desktop com `pywinauto`, `pyautogui` e captura de tela).
- Python `>= 3.13`.
- ERP Consinco instalado com acesso ao executavel:
  - Operador (`Operador.exe`)
- Credenciais validas de Consinco, SMTP e API Sinfonia.

## Instalacao
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuracao (.env)
Crie o arquivo `.env` na raiz com base em `.env.example`.

Exemplo de campos utilizados:

```env
# Processo
PROCESSO_DATA_EMISSAO_FILTRO="01/01/2026"            # Por padrao e D-1 (formato dd/mm/aaaa)

# Consinco
ERP_CONSINCO_LOGIN="@login"
ERP_CONSINCO_SENHA="@senha"

# Caminhos
CAMINHO_EXE_ERP_MODULO_OPERADOR="C:\C5Client\Financeiro\Operador.exe"

# E-mail
ENVIAR_EMAIL=False
DESTINATARIOS=['@destinatario1', '@destinatario2']

# SMTP
SMTP_FROM="@from"
SMTP_SERV="@server"
SMTP_USER="@user"
SMTP_PSWD="@password"
SMTP_PORT=25

# Sinfonia
SINFONIA_BASE_URL="https://sinfonia.live/api"
SINFONIA_TOKEN_API_MASTER="@token"
```

## Execucao
```bash
python main.py
```

## Logs
- Logs sao gerados em tempo de execucao com `loguru`.
- Arquivos de log salvos em `logs/logs_DD_MM_AAAA.log` com rotacao diaria e retencao de 30 dias.
- Em caso de falha, verifique:
  - credenciais do Consinco, SMTP e Sinfonia;
  - caminho do executavel do Operador;
  - estabilidade da tela (resolucao/escala) para automacao UI;
  - imagens de referencia em `resources/images/` (botoes podem mudar de aparencia).

## Contato
Duvidas ou sugestoes: contato@27devs.com
