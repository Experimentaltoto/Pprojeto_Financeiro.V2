# PRD — Sistema Financeiro Experimental

## Objetivo
Construir um sistema financeiro a partir de planilhas enviadas pelo usuário. O sistema conseguirá gerar demonstrativos de fluxo de caixa, DRE, contas a pagar e contas a receber.

## 1. Visão do produto

Aplicação web para consolidar as informações financeiras de um comércio varejista e disponibilizá-las online para acompanhamento e análise. A primeira versão prioriza funcionamento, confiabilidade dos dados e facilidade de consulta.

## 2. Objetivos da primeira versão

- Centralizar dados financeiros atualmente distribuídos em planilhas.
- Apresentar fluxo de caixa indireto em períodos semanais e mensais, além da visão detalhada das movimentações e projeções.
- Apresentar DRE mensal e acumulada por período.
- Acompanhar contas a pagar e recebimentos de cartão.
- Permitir análises mensais, trimestrais, semestrais e por intervalo personalizado.
- Incorporar novas fontes de dados progressivamente.

## 3. Fontes de dados confirmadas

- Planilha de recebimentos da máquina de cartões, com valores separados.
- Planilha de extrato bancário, com movimentações categorizadas pela instituição.
- Planilha de contas a pagar com fornecedor, descrição, categoria, valor, vencimento, data de pagamento e situação.

Os primeiros testes utilizarão arquivos com intervalos de datas diferentes. Os formatos e campos definitivos serão documentados depois que as planilhas de exemplo forem fornecidas.

## 4. Fluxo de importação

1. Upload da planilha pela interface Streamlit.
2. Identificação da origem e validação do formato.
3. Processamento, limpeza e padronização por script específico.
4. Detecção de registros duplicados ou já existentes.
5. Separação das duplicidades para análise do proprietário.
6. Gravação dos dados válidos e não duplicados no Supabase por código Python.
7. Registro do resultado da importação.
8. Descarte do arquivo original após a confirmação da carga.

Não haverá etapa de prévia. Um arquivo válido será processado diretamente. Erros críticos deverão interromper toda a importação, exibir uma mensagem acionável e fazer com que o agente solicite ao proprietário o ajuste do arquivo ou da regra de processamento. Os dados somente poderão ser carregados quando estiverem limpos e no formato padronizado.

Arquivos com períodos diferentes ou sobrepostos não poderão gerar duplicidades. Os registros válidos serão inseridos normalmente, sem que as possíveis duplicidades bloqueiem o arquivo inteiro. Cada registro identificado como possível duplicidade ficará separado e pendente até o final do processamento, quando será apresentado ao proprietário para análise e decisão. Nenhuma duplicidade poderá ser inserida, ignorada, substituída ou atualizada automaticamente. Cada importação registrará origem, data, resultado e quantidades de registros inseridos, rejeitados, duplicados e pendentes. Não será necessário armazenar a planilha original.

Movimentações que não puderem ser categorizadas automaticamente serão marcadas como `pendente de classificação`. Os relatórios deverão indicar a quantidade e o valor dessas pendências. A classificação será realizada posteriormente pelo agente. O banco manterá a categoria financeira padronizada pelo sistema como referência para as análises.

## 5. Tecnologia

- Banco de dados: PostgreSQL no Supabase.
- Front-end e publicação: Streamlit.
- Entrada de dados: upload de planilhas pelo Streamlit.
- Processamento e inserção de dados: scripts Python específicos por fonte.
- Consulta, inspeção e validação do conteúdo do Supabase pelo agente: Supabase MCP.
- O MCP não será utilizado para inserir ou alterar os dados financeiros; escritas no banco serão executadas programaticamente por Python.
- Frequência esperada de atualização: semanal ou mensal.

## 6. Páginas da primeira versão

- Visão geral.
- Fluxo de caixa.
- DRE.
- Contas a pagar.
- Contas a receber.
- Pendências de classificação.
- Upload e histórico das importações.

A aplicação abrirá na visão geral com o mês atual selecionado.

## 7. Indicadores da visão geral

- Saldo disponível.
- Total de entradas.
- Total de saídas.
- Resultado do período.
- Total de contas a pagar.
- Recebimentos de cartão pendentes.
- Comparação com o mês anterior.

## 8. Fluxo de caixa

O demonstrativo principal de fluxo de caixa utilizará o método indireto e poderá ser apurado semanal ou mensalmente. Ele partirá do resultado da DRE gerencial e realizará os ajustes necessários até chegar à variação de caixa do período. A estrutura prevista será:

1. Resultado do período.
2. Ajustes de itens sem efeito no caixa.
3. Variações de ativos e passivos operacionais.
4. Caixa gerado ou consumido pelas atividades operacionais.
5. Fluxo das atividades de investimento.
6. Fluxo das atividades de financiamento.
7. Variação líquida de caixa.
8. Saldo inicial e saldo final.

Como as fontes iniciais ainda não contêm todas as contas necessárias ao método indireto, o demonstrativo deverá ser identificado como parcial até que sejam disponibilizados, entre outros, dados de contas a receber, estoques, fornecedores e demais ativos e passivos relevantes. A apuração semanal dependerá de saldos de abertura e fechamento ou movimentações que permitam calcular as variações patrimoniais de cada semana. Quando uma fonte possuir apenas fechamento mensal, o sistema deverá informar que a visão semanal está incompleta.

Para impedir dupla contagem, aportes, retiradas e parcelas de empréstimos exibidos na DRE gerencial deverão ser retirados do fluxo operacional durante a conciliação do método indireto e apresentados uma única vez nas atividades de financiamento.

Além do demonstrativo indireto, a análise detalhada das movimentações de caixa apresentará:

- Evolução diária do saldo.
- Entradas e saídas por categoria.
- Comparação com o mês anterior.
- Projeção baseada nas contas a pagar futuras.
- Atalhos de projeção para 30, 60 e 90 dias.
- Intervalo personalizado.
- Tabela detalhada dos lançamentos.

Na primeira versão, o saldo será calculado exclusivamente com as contas e movimentações presentes nas planilhas fornecidas.

## 9. DRE

A DRE utilizará o regime de competência e terá a estrutura inicial:

1. Faturamento bruto.
2. Deduções, devoluções e impostos sobre vendas.
3. Receita líquida.
4. Custo das mercadorias vendidas (CMV).
5. Taxas de cartão.
6. Lucro bruto.
7. Despesas operacionais.
8. Resultado financeiro.
9. Resultado líquido.

Cada linha será comparada somente com o mês imediatamente anterior. Enquanto não houver fonte para o CMV, a DRE indicará que o resultado é parcial e não representa o resultado líquido definitivo. Dados de impostos, cancelamentos e devoluções serão incorporados quando suas fontes forem disponibilizadas.

Por se tratar de um sistema experimental, aportes e retiradas dos proprietários também serão exibidos na DRE gerencial, além do fluxo de caixa. Essa apresentação é uma regra gerencial do MVP e não corresponde à classificação contábil convencional.

Na primeira versão, pagamentos de empréstimos serão registrados e apresentados pelo valor total da parcela como despesa, sem separar amortização do principal e juros. Essa separação poderá ser implementada posteriormente. Por esse motivo, a DRE deverá ser identificada como gerencial e experimental.

## 10. Tratamento das vendas em cartão

- O valor bruto da venda será reconhecido como faturamento na DRE.
- As taxas da operadora serão reconhecidas como custo.
- O recebimento efetivo será considerado no fluxo de caixa quando ocorrer.
- Venda, recebível e crédito bancário deverão ser conciliados para impedir dupla contagem.

## 11. Contas a pagar

As contas serão separadas por situação:

- Pendentes.
- Vencidas.
- Pagas.

As contas futuras alimentarão a projeção do fluxo de caixa.

## 12. Contas a receber

Contas a receber terão uma página própria. Inicialmente, a página utilizará os recebíveis disponíveis nas planilhas de cartões. Novas modalidades de recebimento serão incorporadas conforme suas fontes forem disponibilizadas.

## 13. Filtros e exportação

- Mês atual selecionado por padrão.
- Filtros mensais, trimestrais, semestrais e por intervalo personalizado.
- Exportação dos dados filtrados e relatórios em Excel ou CSV.

## 14. Plano de contas inicial

O plano de contas utilizará grupos e subcategorias. A estrutura inicial será:

- Receitas de vendas.
- Deduções, impostos e devoluções.
- CMV.
- Taxas de cartão.
- Despesas com pessoal.
- Ocupação, incluindo aluguel, energia, água e condomínio.
- Despesas administrativas.
- Vendas e marketing.
- Tecnologia e manutenção.
- Tarifas, juros e receitas financeiras.
- Outras receitas e despesas.

Fretes e logística não serão apresentados como grupo específico nas análises da primeira versão. As subcategorias permitirão detalhar os valores dentro de cada grupo principal.

## 15. Inclusões, correções e classificação

Inclusões e correções de lançamentos, assim como a resolução das pendências de classificação, serão realizadas pelo agente por rotinas Python. A primeira versão não terá edição direta desses registros pela interface. Possíveis duplicidades dependerão da decisão do proprietário antes de qualquer tratamento.

## 16. Acesso e segurança

A primeira versão será de uso do proprietário, não terá login e poderá permanecer em endereço público durante os testes. Essa decisão é temporária e envolve risco de exposição dos dados financeiros. Credenciais, chaves administrativas, dados pessoais e informações bancárias sensíveis não deverão ser exibidos no front-end nem armazenados no código-fonte.

## 17. Requisitos de apresentação

- Interface projetada prioritariamente para uso em computador.
- Valores monetários apresentados em reais (R$).
- Datas apresentadas no padrão brasileiro `DD/MM/AAAA`.

## 18. Critérios de aceite do MVP

O MVP será considerado funcional quando atender aos seguintes critérios:

1. Permitir o upload das três fontes iniciais pelo Streamlit.
2. Validar, limpar e padronizar os arquivos por rotinas Python antes da gravação.
3. Interromper arquivos com erro crítico e apresentar informação suficiente para o ajuste.
4. Inserir os registros válidos sem bloquear o arquivo por causa de possíveis duplicidades.
5. Manter as possíveis duplicidades separadas e apresentá-las ao proprietário no final do processamento.
6. Registrar o resultado de cada importação e descartar o arquivo original após uma carga bem-sucedida.
7. Permitir ao agente consultar e validar os dados do Supabase por MCP, mantendo todas as inserções e alterações em rotinas Python.
8. Abrir a visão geral no mês atual e apresentar os indicadores definidos neste documento.
9. Gerar a DRE gerencial e indicar claramente quando o resultado estiver parcial.
10. Gerar o fluxo de caixa indireto semanal e mensal, indicando quando faltarem fontes para sua conclusão.
11. Conciliar saldo inicial, variação líquida e saldo final quando todas as informações do período estiverem disponíveis.
12. Apresentar o detalhamento das movimentações, as projeções e as páginas de contas a pagar e a receber.
13. Aplicar filtros de período e permitir exportações em Excel ou CSV.
14. Fazer com que os totais exibidos possam ser conferidos contra os registros carregados no Supabase.

## 19. Fora do escopo inicial

- Login e gestão de usuários.
- Otimização específica para celulares.
- Edição manual de lançamentos pelo Streamlit.
- Armazenamento permanente das planilhas originais.
- Integrações automáticas com bancos e operadoras de cartão.
- DRE contábil definitiva enquanto não houver todas as fontes necessárias.
- Separação entre principal e juros das parcelas de empréstimos.
- Tratamento de fretes e logística como grupo analítico próprio.

## 20. Requisitos de qualidade

- Valores financeiros deverão preservar a precisão decimal e não poderão utilizar arredondamentos binários inadequados.
- Datas, valores e categorias deverão ser normalizados antes da gravação.
- Credenciais do Supabase deverão permanecer fora do código-fonte e do front-end.
- Mensagens de erro deverão identificar o arquivo, a causa e a ação necessária.
- Totais dos relatórios deverão permitir rastreamento até os lançamentos que os compõem.
- O volume e o tempo de processamento de cada importação deverão ser registrados durante os testes para definir metas de desempenho posteriores.

## 21. Dependências e evoluções futuras

- Campos e formatos exatos das planilhas.
- Fonte e regra de cálculo do CMV.
- Mapeamento das descrições das planilhas para grupos e subcategorias do plano de contas.
- Regras de conciliação entre cartões e extrato bancário.
- Identificadores definitivos para detecção de possíveis duplicidades.
- Histórico inicial a importar.
- Regras detalhadas para cálculo do saldo bancário inicial.
- Separação futura entre principal e juros nas parcelas de empréstimos.
- Fontes das variações patrimoniais necessárias ao fluxo de caixa indireto.
- Volume máximo de linhas por arquivo, a ser medido durante os testes.
