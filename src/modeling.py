import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def dividir_dados(df, target, test_size=0.2, random_state=42):
    """
    Divide o DataFrame em variáveis independentes (X) e dependente (y), 
    e em conjuntos de treino e teste.
    """
    X = df.drop(target, axis=1)
    y = df[target]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def treinar_modelo(modelo, X_train, y_train):
    """
    Treina o modelo com os dados de treino.
    """
    modelo.fit(X_train, y_train)
    return modelo

def avaliar_modelo(modelo, X_test, y_test):
    """
    Avalia o modelo com as métricas de classificação.
    """
    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted')
    rec = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print("Accuracy:", acc)
    print("Precision:", prec)
    print("Recall:", rec)
    print("F1 Score:", f1)
    
    return {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1}

def matriz_confusao(modelo, X_test, y_test):
    """
    Plota a matriz de confusão.
    """
    y_pred = modelo.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predito')
    plt.ylabel('Verdadeiro')
    plt.title('Matriz de Confusão')
    plt.show()

def relatorio_classificacao(modelo, X_test, y_test):
    """
    Gera e imprime o relatório de classificação.
    """
    y_pred = modelo.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(report)
    return report

def ajuste_hiperparametros(modelo, param_grid, X_train, y_train, cv=5, scoring='accuracy'):
    """
    Realiza busca em grade (GridSearchCV) para ajuste de hiperparâmetros.
    """
    grid_search = GridSearchCV(modelo, param_grid, cv=cv, scoring=scoring)
    grid_search.fit(X_train, y_train)
    print("Melhores parâmetros:", grid_search.best_params_)
    print("Melhor score:", grid_search.best_score_)
    return grid_search.best_estimator_
