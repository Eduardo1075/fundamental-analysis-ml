import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analisar_variaveis_nulas(df):
    """
    Exibe a contagem e percentual de variáveis nulas no DataFrame.
    """
    nulos = df.isnull().sum()
    percentual = (nulos / len(df)) * 100
    nulos_df = pd.DataFrame({'nulos': nulos, 'percentual': percentual})
    nulos_df = nulos_df[nulos_df['nulos'] > 0].sort_values(by='percentual', ascending=False)
    print(nulos_df)
    return nulos_df

def visualizar_distribuicoes(df, colunas, bins=30):
    """
    Plota histogramas para as colunas numéricas especificadas.
    """
    for coluna in colunas:
        plt.figure(figsize=(8, 4))
        sns.histplot(df[coluna].dropna(), bins=bins, kde=True)
        plt.title(f'Distribuição de {coluna}')
        plt.xlabel(coluna)
        plt.ylabel('Frequência')
        plt.show()

def visualizar_boxplots(df, colunas):
    """
    Plota boxplots para as colunas numéricas especificadas.
    """
    for coluna in colunas:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=df[coluna])
        plt.title(f'Boxplot de {coluna}')
        plt.xlabel(coluna)
        plt.show()

def correlacao_heatmap(df, metodo='pearson', annot=True, cmap='coolwarm'):
    """
    Plota um mapa de calor com a matriz de correlação.
    """
    plt.figure(figsize=(12, 8))
    matriz_corr = df.corr(method=metodo)
    sns.heatmap(matriz_corr, annot=annot, cmap=cmap)
    plt.title(f'Heatmap de Correlação ({metodo})')
    plt.show()
    return matriz_corr

def relatorio_estatistico(df):
    """
    Gera um resumo estatístico descritivo para o DataFrame.
    """
    resumo = df.describe().T
    resumo['missing'] = df.isnull().sum()
    resumo['missing_percent'] = (resumo['missing'] / len(df)) * 100
    print(resumo)
    return resumo
