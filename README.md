# Taxas P2P

Projeto para obter automaticamente as taxas P2P de compra e venda de USDT.

## Corretoras

- Binance (VES)
- Bybit (BRL)

## Objetivo

Buscar automaticamente as melhores taxas utilizando critérios próprios e atualizar uma planilha do Google Sheets a cada 15 minutos.

## Estrutura

- main.py → executa todo o projeto
- binance_ves.py → taxa Binance VES
- bybit_brl.py → taxa Bybit BRL
- sheets.py → integração com Google Sheets
- config.py → configurações
- requirements.txt → dependências
