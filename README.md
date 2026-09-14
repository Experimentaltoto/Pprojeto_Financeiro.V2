# Normalizador de planilhas financeiras

O script converte uma fonte por vez para um CSV canônico, preservando a linha
original em `source_payload` para auditoria e usando representação decimal em
texto (nunca `float`). A validação ocorre antes de qualquer escrita; se uma
linha obrigatória estiver inválida, o CSV de destino permanece inalterado.

## Instalação e uso

```powershell
python -m pip install -r requirements.txt
python scripts/normalize_spreadsheets.py Dados/Vendas_Stone_Set.xlsx saida/vendas.csv
python scripts/normalize_spreadsheets.py Dados/Extrato_Lançamentos_Set.xlsx saida/extrato.csv
python scripts/normalize_spreadsheets.py relatorio_tiny.xls saida/pagamentos.csv --source tiny --category-map categorias.json
```

`categorias.json` é opcional e tem a forma abaixo. Categorias sem um mapeamento
confiável recebem exatamente `pendente de classificação`.

```json
{
  "aluguel": "Ocupação",
  "energia elétrica": "Ocupação"
}
```

Os contratos atualmente validados são:

- Stone: primeira linha com `STONECODE`, `DATA DA VENDA`, `VALOR BRUTO`,
  `VALOR LIQUIDO` e `ULTIMO STATUS`. O CSV retém bruto, líquido e taxas em
  colunas separadas para não confundir faturamento com recebimento de caixa.
- Extrato: a rotina encontra a linha de cabeçalho com `Data`, `Lançamento` e
  `Valor (R$)` (o exemplo a possui na linha 10). `SALDO ANTERIOR` é emitido
  como `bank_balance`; os demais lançamentos ficam pendentes de classificação
  até existir mapa confiável.
- Tiny: requer `.xls` íntegro e uma linha de cabeçalho com `Fornecedor`,
  `Descrição`, `Categoria`, `Valor`, `Vencimento`, `Data de pagamento` e
  `Situação`. Este contrato é uma validação explícita e deve ser ajustado caso
  a exportação oficial use outros nomes.

`candidate_duplicate_key` é apenas uma chave candidata; não elimina, altera ou
resolve registros. A separação contra dados já importados deve acontecer na
rotina de carga do banco.
