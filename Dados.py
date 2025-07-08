import pandas as pd
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

def baixar_dados(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    compressed_file = BytesIO(response.content)
    df = pd.read_csv(compressed_file, compression='gzip')
    return df

def preparar_dados(df, estados=None):
    df_estados = df[df['place_type'] == 'state'].copy()
    if estados is None:
        estados = df_estados['state'].unique()
    df_selecionados = df_estados[df_estados['state'].isin(estados)].copy()
    df_selecionados.loc[:, 'date'] = pd.to_datetime(df_selecionados['date'])
    return df_selecionados

def plot_series_temporais(df, estados):
    plt.figure(figsize=(14, 6))
    for estado in estados:
        dados_estado = df[df['state'] == estado]
        plt.plot(dados_estado['date'], dados_estado['last_available_confirmed'], label=estado)
    plt.title('Casos Confirmados por Estado')
    plt.xlabel('Data')
    plt.ylabel('Casos Confirmados')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_histograma(df, coluna):
    plt.figure(figsize=(10,5))
    nome_legivel = 'Casos Confirmados' if 'confirmed' in coluna else 'Mortes Confirmadas'
    sns.histplot(df[coluna], bins=30, kde=True)
    plt.title(f'Distribuição de {nome_legivel}')
    plt.xlabel(nome_legivel)
    plt.ylabel('Frequência')
    plt.show()

def plot_boxplot_por_estado(df, coluna):
    plt.figure(figsize=(12,6))
    nome_legivel = 'Casos Confirmados' if 'confirmed' in coluna else 'Mortes Confirmadas'
    sns.boxplot(x='state', y=coluna, data=df)
    plt.title(f'Boxplot de {nome_legivel} por Estado')
    plt.xlabel('Estado')
    plt.ylabel(nome_legivel)
    plt.show()

def plot_barras_totais(df, estados, coluna='last_available_confirmed', titulo=None):
    ultimos_dias = df.groupby('state').last().loc[estados]
    plt.figure(figsize=(12,6))
    nome_legivel = 'Casos Confirmados' if 'confirmed' in coluna else 'Mortes Confirmadas'
    sns.barplot(x=ultimos_dias.index, y=ultimos_dias[coluna])
    plt.title(titulo or f'Total de {nome_legivel} por Estado (Último Dia)')
    plt.ylabel(nome_legivel)
    plt.xlabel('Estado')
    plt.show()

def calcular_taxa_mortalidade(df, estados):
    ultimos = df.groupby('state').last().loc[estados]
    ultimos['taxa_mortalidade'] = ultimos['last_available_deaths'] / ultimos['last_available_confirmed']
    print('Taxa de Mortalidade por Estado (último dia disponível):')
    print(ultimos[['last_available_confirmed', 'last_available_deaths', 'taxa_mortalidade']])
    return ultimos

def calcular_crescimento_percentual_medio(df, estados, window=7):
    print(f'Crescimento percentual médio diário dos casos (janela {window} dias):')
    for estado in estados:
        dados_estado = df[df['state'] == estado].sort_values('date')
        dados_estado['novos_casos'] = dados_estado['last_available_confirmed'].diff()
        dados_estado['pct_crescimento'] = dados_estado['novos_casos'] / dados_estado['last_available_confirmed'].shift(1)
        media_crescimento = dados_estado['pct_crescimento'].rolling(window).mean().iloc[-1]
        print(f'{estado}: {media_crescimento:.4f}')

def calcular_crescimento_percentual_medio_mortes(df, estados, window=7):
    print(f'Crescimento percentual médio diário das mortes (janela {window} dias):')
    for estado in estados:
        dados_estado = df[df['state'] == estado].sort_values('date')
        dados_estado['novas_mortes'] = dados_estado['last_available_deaths'].diff()
        dados_estado['pct_crescimento_mortes'] = dados_estado['novas_mortes'] / dados_estado['last_available_deaths'].shift(1)
        media_crescimento = dados_estado['pct_crescimento_mortes'].rolling(window).mean().iloc[-1]
        print(f'{estado}: {media_crescimento:.4f}')

def plot_heatmap_correlacao(df):
    cols = ['last_available_confirmed', 'last_available_deaths', 'estimated_population']
    corr = df[cols].corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Mapa de Correlação entre Variáveis')
    plt.show()

def plot_taxa_letalidade(df, estados):
    df = df.copy()
    df['taxa_letalidade'] = df['last_available_deaths'] / df['last_available_confirmed']
    plt.figure(figsize=(14,6))
    for estado in estados:
        dados_estado = df[df['state'] == estado]
        plt.plot(dados_estado['date'], dados_estado['taxa_letalidade'], label=estado)
    plt.title('Evolução da Taxa de Letalidade por Estado')
    plt.xlabel('Data')
    plt.ylabel('Taxa de Letalidade')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    url = 'https://data.brasil.io/dataset/covid19/caso_full.csv.gz'
    df = baixar_dados(url)

    estados = None  # todos os estados

    df_selecionados = preparar_dados(df, estados)

    plot_series_temporais(df_selecionados, df_selecionados['state'].unique())

    plot_histograma(df_selecionados, 'last_available_confirmed')

    plot_boxplot_por_estado(df_selecionados, 'last_available_confirmed')

    plot_barras_totais(df_selecionados, df_selecionados['state'].unique(), coluna='last_available_confirmed')

    plot_barras_totais(df_selecionados, df_selecionados['state'].unique(), coluna='last_available_deaths',
                      titulo='Total de Mortes Confirmadas por Estado (Último Dia)')

    taxa_mortalidade_df = calcular_taxa_mortalidade(df_selecionados, df_selecionados['state'].unique())

    calcular_crescimento_percentual_medio(df_selecionados, df_selecionados['state'].unique())

    calcular_crescimento_percentual_medio_mortes(df_selecionados, df_selecionados['state'].unique())

    plot_heatmap_correlacao(df_selecionados)

    plot_taxa_letalidade(df_selecionados, df_selecionados['state'].unique())

if __name__ == '__main__':
    main()