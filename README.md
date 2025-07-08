# Análise Exploratória de Dados COVID-19 no Brasil

Este projeto é uma análise exploratória dos dados públicos de COVID-19 no Brasil, utilizando Python, Pandas, Matplotlib e Seaborn. O objetivo é demonstrar habilidades em manipulação, visualização e análise de dados, com foco na comparação entre estados brasileiros.

---

## O que foi feito

- Download e limpeza dos dados oficiais de COVID-19 do portal Brasil.IO.
- Filtragem dos dados para análises por estado.
- Visualizações diversas:
  - Séries temporais de casos confirmados e mortes.
  - Histogramas e boxplots para entender distribuições e variações por estado.
  - Gráficos de barras com totais de casos e mortes.
  - Heatmap de correlação entre variáveis.
  - Evolução da taxa de letalidade ao longo do tempo.
- Cálculo de métricas importantes:
  - Taxa de mortalidade por estado (último dia disponível).
  - Crescimento percentual médio diário de casos e mortes.
- Organização do código em funções para melhor reutilização e legibilidade.

---

## Tecnologias usadas

- Python 3.12
- Pandas
- Requests
- Matplotlib
- Seaborn

---

## Como executar

1. Clone este repositório.
2. Instale as dependências (exemplo com pip):

   ```bash
   pip install pandas requests matplotlib seaborn
