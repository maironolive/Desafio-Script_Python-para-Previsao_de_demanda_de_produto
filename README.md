# Script Python para previsão de demanda de um produto específico

## 1. Desafio proposto

Uma das questões do desafio técnico da Indicium Academy AI tem como objetivo construir um modelo baseline para previsão mensal de demanda de um produto específico, auxiliando no planejamento de estoque e na tomada de decisões de compra.

O produto analisado foi a **Bússola de Bordo 702**, utilizando uma média móvel dos últimos três meses como método de previsão.

A solução utiliza dados armazenados no PostgreSQL e um script Python para calcular as previsões, comparar os resultados com as vendas reais e avaliar o desempenho por meio da métrica MAE (Mean Absolute Error).

## 2. Objetivos

- Construir um dataset unificado a partir dos arquivos products.csv, product_variants, orders.csv e order_items.csv.
- Considerar exclusivamente o produto Bússola de Bordo 702.
- Realizar previsões em base mensal.
- Utilizar dados de treinamento até 31/12/2025.
- Prever as vendas de janeiro, fevereiro e março de 2026.
- Comparar as previsões com os valores reais utilizando o MAE.
- Evitar data leakage durante a geração das previsões.
- Avaliar a adequação e as limitações do modelo baseline.

## 3. Tecnologias utilizadas

- **Python 3**: implementação da lógica de previsão e avaliação.
- **PostgreSQL**: armazenamento e consulta do histórico mensal de vendas.
- **psycopg2**: conexão entre Python e PostgreSQL.
- **DBeaver**: ferramenta gráfica para consultar os dados, executar comandos SQL e validar os resultados.

## 4. Premissas do desafio

- O período de treinamento inclui dados até 31/12/2025.
- O período de teste corresponde ao primeiro trimestre de 2026.
- A previsão é realizada em base mensal.
- Apenas o produto Bússola de Bordo 702 é considerado.
- O modelo baseline utiliza a média móvel dos últimos três meses.
- A previsão de cada mês utiliza somente informações disponíveis antes da data prevista.
- O desempenho é avaliado por meio do MAE.
- A soma total das previsões para o primeiro trimestre de 2026 foi informada como 112 unidades.

## 5. Estrutura dos dados

### 5.1. Fontes utilizadas

A construção do dataset unificado considera as seguintes fontes:

- **products.csv**: informações cadastrais dos produtos.
- **product_variants**: informações sobre as variantes dos produtos.
- **orders.csv**: informações dos pedidos.
- **order_items.csv**: itens e quantidades associados aos pedidos.

Essas fontes permitem relacionar os produtos vendidos aos respectivos pedidos e consolidar as quantidades em uma série temporal mensal.

### 5.2. Dataset utilizado pelo modelo

O script Python consulta a tabela staging.demanda_bussola_702, que contém os dados mensais preparados para a previsão.

A consulta utiliza duas colunas:

- **mes**: mês de referência das vendas.
- **quantidade_vendida**: quantidade vendida no respectivo mês.

A tabela deve estar previamente construída e conter o histórico necessário para treinamento e validação.

## 6. Script Python — Previsão de demanda

### 6.1. Objetivo

O script realiza a previsão mensal das vendas da Bússola de Bordo 702 para o primeiro trimestre de 2026, utilizando uma média móvel dos três meses anteriores.

O código é responsável por consultar os dados no PostgreSQL, separar os períodos, calcular as previsões, comparar os resultados com os valores reais e apresentar o MAE.

### 6.2. Configuração do banco de dados

A conexão utiliza os seguintes parâmetros:

- **Host:** localhost
- **Porta:** 5432
- **Database:** postgres
- **Usuário:** postgres
- **Tabela de origem:** staging.demanda_bussola_702

A senha é obtida por meio da variável de ambiente LIGHTHOUSE_DB_PASSWORD, evitando seu armazenamento diretamente no código.

No PowerShell, configure a variável antes da execução:

```powershell
$env:LIGHTHOUSE_DB_PASSWORD = "SUA_SENHA"
```

### 6.3. Etapas do processamento

1. Valida a configuração da senha.
2. Conecta-se ao PostgreSQL.
3. Consulta o histórico mensal de vendas.
4. Organiza os dados por mês.
5. Define o período de treinamento até dezembro de 2025.
6. Define janeiro, fevereiro e março de 2026 como período de teste.
7. Calcula as previsões utilizando a média móvel dos três meses anteriores.
8. Calcula os erros absolutos entre os valores reais e previstos.
9. Calcula o MAE do trimestre.
10. Exibe os resultados no terminal.

## 7. Modelo baseline — Média móvel de três meses

### 7.1. Funcionamento

A média móvel utiliza as vendas dos três meses anteriores para estimar a quantidade que será vendida no mês seguinte.

A fórmula utilizada é:

```text
Previsão do mês =
(Vendas do mês anterior
 + Vendas de dois meses anteriores
 + Vendas de três meses anteriores) / 3
```

### 7.2. Aplicação ao primeiro trimestre de 2026

- **Janeiro de 2026:** utiliza as vendas reais de outubro, novembro e dezembro de 2025.
- **Fevereiro de 2026:** utiliza as vendas de novembro e dezembro de 2025 e a previsão de janeiro de 2026.
- **Março de 2026:** utiliza as vendas de dezembro de 2025 e as previsões de janeiro e fevereiro de 2026.

Essa abordagem permite gerar as três previsões sem utilizar os valores reais dos meses do período de teste.

## 8. Prevenção de data leakage

O data leakage ocorre quando informações que não estariam disponíveis no momento da previsão são utilizadas indevidamente no modelo.

Para evitar esse problema:

- O treinamento considera somente os dados disponíveis até dezembro de 2025.
- Os valores reais de janeiro, fevereiro e março de 2026 não são utilizados no cálculo das previsões.
- A previsão de janeiro utiliza os três meses anteriores do histórico de treinamento.
- As previsões de fevereiro e março utilizam as previsões anteriores, em vez das vendas reais dos meses de teste.
- Os valores reais do primeiro trimestre de 2026 são utilizados somente na etapa de avaliação.

Dessa forma, a validação simula uma situação em que as vendas futuras ainda são desconhecidas.

## 9. Avaliação do modelo — MAE

### 9.1. Definição

O MAE (Mean Absolute Error) representa a média dos erros absolutos entre as quantidades reais e previstas.

A fórmula é:

```text
MAE = Soma dos erros absolutos / Número de meses avaliados
```

O erro absoluto de cada mês é calculado por:

```text
Erro absoluto = |Venda real - Previsão|
```

### 9.2. Interpretação

- Um MAE menor indica previsões mais próximas dos valores reais.
- Um MAE maior indica maior diferença entre as quantidades previstas e observadas.
- Como a previsão é mensal e a variável representa unidades vendidas, o MAE é interpretado em unidades do produto por mês.

O script apresenta os valores reais, as previsões e os erros absolutos de cada mês, além do MAE consolidado do primeiro trimestre de 2026.

O valor numérico do MAE deve ser obtido a partir da execução do script com os dados reais do banco de dados.

## 10. Resultado da Questão 6.2

A soma total da previsão de vendas para a Bússola de Bordo 702 durante o primeiro trimestre de 2026 foi informada como:

**112 unidades.**

Esse valor corresponde à soma das previsões mensais de janeiro, fevereiro e março de 2026, arredondada para um número inteiro.

## 11. Respostas conceituais do desafio

### 11.1. Como o baseline foi construído?

O baseline foi construído utilizando uma média móvel dos últimos três meses de vendas da Bússola de Bordo 702. Primeiro, as vendas foram agregadas mensalmente e o período de treinamento foi definido até 31/12/2025. A previsão de cada mês do primeiro trimestre de 2026 foi calculada com base nos três valores anteriores disponíveis.

### 11.2. Como foi evitado o data leakage?

O período de teste foi mantido separado do treinamento, considerando janeiro, fevereiro e março de 2026 apenas para validação. A previsão de janeiro utilizou os três últimos meses de 2025 e, para os meses seguintes, foram utilizadas as previsões anteriores, evitando que os valores reais de 2026 influenciassem o modelo.

### 11.3. Qual é uma limitação do modelo proposto?

A principal limitação é que a média móvel considera apenas os três meses anteriores e não captura tendências, sazonalidade ou outros fatores que possam influenciar a demanda, podendo apresentar previsões menos precisas em períodos de crescimento, queda ou comportamento sazonal das vendas.

## 12. Execução do script

### 12.1. Instalação da dependência

```bash
python -m pip install psycopg2-binary
```

### 12.2. Configuração da senha

No PowerShell:

```powershell
$env:LIGHTHOUSE_DB_PASSWORD = "SUA_SENHA"
```

### 12.3. Execução

Salve o código em um arquivo chamado questao_6.py e execute:

```bash
python questao_6.py
```

O script exibirá uma tabela contendo o mês de referência, as vendas reais, as previsões, os erros absolutos e o MAE do período de teste.

## 13. Validação no DBeaver

O DBeaver pode ser utilizado para verificar a tabela de origem e consultar os dados mensais utilizados pelo modelo.

Exemplo de consulta:

```sql
SELECT
    mes,
    quantidade_vendida
FROM staging.demanda_bussola_702
ORDER BY mes;
```

Para conferir o período de teste:

```sql
SELECT
    mes,
    quantidade_vendida
FROM staging.demanda_bussola_702
WHERE mes >= DATE '2026-01-01'
  AND mes <= DATE '2026-03-01'
ORDER BY mes;
```

Essas consultas permitem inspecionar o histórico e os valores reais utilizados na avaliação.

## 14. Limitações e pontos de atenção

- O modelo utiliza somente os três meses anteriores para calcular cada previsão.
- Não considera sazonalidade, tendências de longo prazo, preços, promoções ou disponibilidade de estoque.
- O método depende da existência de três meses anteriores para cada previsão.
- A qualidade do resultado depende da consistência e da completude do histórico mensal.
- O MAE deve ser interpretado considerando o volume de vendas e o contexto do produto.
- A previsão não garante que a demanda real será igual à quantidade estimada.
- O script pressupõe que a tabela staging.demanda_bussola_702 já foi construída e contém os dados necessários.

## 15. Considerações finais

A solução implementa um baseline simples e reproduzível para estimar a demanda mensal da Bússola de Bordo 702.

A média móvel de três meses fornece uma referência inicial para o planejamento de estoque e permite avaliar o desempenho preditivo por meio do MAE. A separação temporal entre treinamento e teste, combinada com o uso das previsões anteriores nos meses subsequentes, evita o uso indevido de vendas futuras.

Embora seja útil como referência inicial, o baseline pode ser aprimorado com métodos que considerem sazonalidade, tendências e variáveis adicionais relacionadas à demanda.

**Fluxo geral do modelo:**

```text
products.csv
product_variants
orders.csv
order_items.csv
        |
        v
Construção do dataset unificado
        |
        v
staging.demanda_bussola_702
        |
        v
Consulta do histórico mensal
        |
        v
Treinamento até 31/12/2025
        |
        v
Média móvel de três meses
        |
        v
Previsões de janeiro a março de 2026
        |
        v
Comparação com vendas reais
        |
        v
Cálculo do MAE e avaliação do baseline
```

---
### 🚀 Projetos e Portfólio
Desenvolvo projetos práticos envolvendo análise de dados, dashboards, indicadores de desempenho, ETL e visualização analítica, conectando tecnologia e problemas reais de negócio.

- 📊 [Portfólio com análises no Medium](https://medium.com/@maironhenrique)
- 📈 [Portfólio com Dashboards](https://app.xperiun.com/in/maironhenrique)
---
### 📫 Contato
**E-mail**: maironhenrique@hotmail.com  
**LinkedIn**: https://www.linkedin.com/in/maironhenriquedeoliveira

#### <p align="left"> <code>Transformando dados em insights para decisões melhores.</code></p>
