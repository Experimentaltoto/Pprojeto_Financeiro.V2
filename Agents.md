# AGENTS.md — Sistema Financeiro Experimental

Estas instruções orientam qualquer agente que trabalhe neste repositório. O
requisito de produto completo está em [PRD.md](PRD.md); em caso de conflito,
o PRD prevalece e a divergência deve ser sinalizada antes da implementação.

## Contexto e estado atual

O projeto está no estágio de descoberta/implementação inicial. Ainda não há
aplicação, esquema de banco, dependências ou testes. As fontes de exemplo
estão em `Dados/`:

- `Vendas_Stone_Set.xlsx`: vendas de cartão; a primeira linha contém os
  cabeçalhos e há valores monetários em formato brasileiro.
- `Extrato_Lançamentos_Set.xlsx`: extrato bancário; metadados ocupam as
  primeiras linhas e o cabeçalho dos lançamentos começa na linha 10.
- `Relatório_Tiny.xls`: contas a pagar em formato Excel legado; confirme a
  estrutura e a biblioteca de leitura antes de implementar seu importador.

Esses arquivos são apenas amostras. Não conclua que layout, colunas ou linhas
de cabeçalho serão permanentes sem registrar a validação correspondente.

## Stack e limites de integração

- Interface e publicação: Streamlit, priorizando desktop.
- Processamento, importação e rotinas de correção: Python.
- Persistência: PostgreSQL no Supabase.
- O Supabase MCP é exclusivamente para consulta, inspeção e validação.
  Nunca o use para inserir, atualizar ou excluir dados financeiros.
- Escritas no banco devem ocorrer apenas por código Python, com transações,
  validações e rastreabilidade.
- Segredos e URLs do Supabase devem vir de variáveis de ambiente ou de um
  arquivo local ignorado pelo Git; nunca do código, do Streamlit ou de logs.

Ao iniciar a aplicação, prefira separar responsabilidades em módulos claros,
por exemplo `app.py`, `pages/`, `src/importers/`, `src/services/`,
`src/repositories/`, `src/models/` e `tests/`. Não crie uma camada complexa
sem necessidade: mantenha as regras de negócio testáveis e fora das páginas
do Streamlit.

## Regras inegociáveis para dados financeiros

- Use `Decimal` (ou `NUMERIC` no PostgreSQL) para dinheiro. Não use `float`
  para cálculos, comparações, conciliação ou totais.
- Normalize datas, valores, textos e categorias antes de persistir. Exiba
  moeda em `R$` e data em `DD/MM/AAAA`.
- Preserve o dado original necessário para auditoria e também o valor
  normalizado; cada total apresentado deve permitir chegar aos lançamentos
  que o compõem.
- Trate uma falha crítica de formato, campos obrigatórios ou normalização como
  falha de toda a importação: não persista uma carga parcial e mostre o
  arquivo, a causa e a ação necessária.
- Registros válidos de um arquivo com duplicidades possíveis continuam aptos
  à carga. Cada possível duplicidade deve ficar pendente e fora das tabelas
  analíticas até decisão explícita do proprietário.
- Nunca insira, descarte, substitua, atualize ou resolva automaticamente uma
  possível duplicidade. Guarde o motivo/critério da sinalização.
- Registros sem categoria confiável recebem exatamente o estado
  `pendente de classificação`; os relatórios devem informar quantidade e
  valor dessas pendências.
- Registre toda importação: origem, período quando conhecido, data/hora,
  resultado, duração e quantidades inseridas, rejeitadas, duplicadas e
  pendentes. Após carga bem-sucedida, descarte o arquivo temporário original;
  não armazene planilhas permanentemente.
- Não exponha em tela, commits, fixtures ou logs dados bancários, CPF/CNPJ,
  identificadores completos de cartão ou credenciais. Dados de exemplo devem
  ser minimizados ou anonimizados quando incluídos em testes.

## Semântica do domínio

- A DRE é gerencial, experimental e por competência. Enquanto não houver
  fonte de CMV, identifique-a claramente como parcial.
- A DRE reconhece venda bruta; taxas de cartão são custo. Aportes, retiradas e
  parcelas de empréstimo são exibidos nela por regra gerencial do MVP.
- Fluxo de caixa é indireto, semanal ou mensal, e deve ser marcado como
  parcial/incompleto quando faltarem saldos ou variações patrimoniais. Evite
  dupla contagem: aportes, retiradas e parcelas de empréstimo entram uma vez
  em financiamento, não no operacional.
- O recebimento de cartão só afeta caixa quando ocorre. Concilie venda,
  recebível e crédito bancário antes de consolidar valores.
- Contas futuras a pagar alimentam projeções de 30, 60, 90 dias e intervalo
  personalizado. Não invente projeções quando não houver dados suficientes.
- A interface não terá edição manual de lançamentos no MVP. Inclusões,
  correções e classificações são rotinas Python; duplicidades sempre aguardam
  decisão do proprietário.

## Desenvolvimento e verificação

Antes de alterar regras de importação, leia o PRD e inspecione uma cópia
segura da fonte real. Documente explicitamente o contrato de cada importador:
origem reconhecida, colunas obrigatórias, conversões, chaves candidatas de
duplicidade, erros críticos e testes de exemplo.

Implemente testes para, no mínimo:

1. conversão de formatos brasileiros de data e moeda;
2. rejeição atômica de arquivos inválidos;
3. separação de possíveis duplicidades sem bloqueio dos registros válidos;
4. classificação pendente e seus totais;
5. conciliação de saldos e prevenção de dupla contagem;
6. rastreabilidade entre relatórios e lançamentos.

Quando os comandos do projeto existirem, execute os testes e a verificação de
formatação/lint relevantes antes de encerrar uma alteração. Não invente
comandos, credenciais ou um esquema de produção. Para toda premissa ainda não
confirmada — especialmente campos do Tiny, CMV, regras de conciliação, saldo
inicial e chaves definitivas de duplicidade — implemente um ponto explícito de
configuração ou peça confirmação.

## Escopo do MVP

As páginas previstas são visão geral, fluxo de caixa, DRE, contas a pagar,
contas a receber, pendências de classificação e upload/histórico. A visão
geral abre no mês atual. Filtros incluem mês, trimestre, semestre e intervalo
personalizado; exportações devem respeitar o filtro e produzir Excel ou CSV.

Login, edição direta no Streamlit, integração automática com bancos ou
operadoras, armazenamento permanente dos arquivos, DRE contábil definitiva e
experiência mobile não fazem parte deste MVP. Não os introduza sem uma decisão
explícita do proprietário.
