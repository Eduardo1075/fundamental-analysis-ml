import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plotar_metricas(resultados):
    """
    Plota um gráfico de barras com as métricas de avaliação do modelo.
    
    Parâmetros:
    - resultados: dicionário com métricas (accuracy, precision, recall, f1).
    """
    metricas = list(resultados.keys())
    valores = list(resultados.values())
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x=metricas, y=valores, palette='viridis')
    plt.ylim(0, 1)
    plt.title('Métricas de Avaliação')
    plt.ylabel('Valor')
    plt.xlabel('Métrica')
    plt.show()

def comparar_modelos(resultados_dict):
    """
    Compara múltiplos modelos em um gráfico de barras.
    
    Parâmetros:
    - resultados_dict: dicionário onde a chave é o nome do modelo e o valor é outro dicionário com as métricas.
    """
    df = pd.DataFrame(resultados_dict).T
    df.plot(kind='bar', figsize=(10, 6))
    
    plt.title('Comparação de Modelos')
    plt.xlabel('Modelos')
    plt.ylabel('Métrica')
    plt.ylim(0, 1)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def salvar_resultados(resultados, caminho='resultados.csv'):
    """
    Salva as métricas em um arquivo CSV.
    
    Parâmetros:
    - resultados: dicionário com as métricas.
    - caminho: caminho do arquivo CSV.
    """
    df = pd.DataFrame([resultados])
    df.to_csv(caminho, index=False)
    print(f"Resultados salvos em {caminho}")
