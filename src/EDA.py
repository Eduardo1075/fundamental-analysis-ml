Extrair e preparar dados financeiros das empresas
import pandas as pd
import os
import zipfile

def extrair_fundamentos(zip_file, extract_folder, empresas):
    os.makedirs(extract_folder, exist_ok=True)

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    fundamentos = {}
    pasta_balancos = os.path.join(extract_folder, 'balancos')
    arquivos = os.listdir(pasta_balancos)

    for arquivo in arquivos:
        nome = arquivo[-9:-4]
        if '11' in nome:
            nome = arquivo[-10:-4]
        if nome in empresas:
            balanco = pd.read_excel(os.path.join(pasta_balancos, arquivo), sheet_name=0)
            balanco.iloc[0, 0] = nome
            balanco.columns = balanco.iloc[0]
            balanco = balanco[1:]
            balanco = balanco.set_index(nome)

            dre = pd.read_excel(os.path.join(pasta_balancos, arquivo), sheet_name=1)
            dre.iloc[0, 0] = nome
            dre.columns = dre.iloc[0]
            dre = dre[1:]
            dre = dre.set_index(nome)


# Filtrar e preparar cotações das empresas          
            fundamentos[nome] = (balanco, dre)
    return fundamentos

def preparar_cotacoes(cotacoes_file, empresas, fundamentos):
    cotacoes_df = pd.read_excel(cotacoes_file)
    cotacoes = {}

    for empresa in cotacoes_df["Empresa"].unique():
        cotacoes[empresa] = cotacoes_df.loc[cotacoes_df['Empresa'] == empresa, :]

    for empresa in empresas[:]:  # faz cópia para evitar erro de remoção em loop
        if cotacoes[empresa].isnull().values.any():
            cotacoes.pop(empresa)
            fundamentos.pop(empresa)

    empresas_validas = list(cotacoes.keys())
    return cotacoes, fundamentos, empresas_validas

# Consolidar fundamentos com cotações
def consolidar_fundamentos(fundamentos, cotacoes):
    for empresa in fundamentos:
        tabela = fundamentos[empresa][0].T
        tabela.index = pd.to_datetime(tabela.index, dayfirst=True, errors='coerce')
        tabela_cotacao = cotacoes[empresa].set_index('Date')[['Adj Close']]
        tabela = tabela.merge(tabela_cotacao, left_index=True, right_index=True)
        tabela.index.name = empresa
        fundamentos[empresa] = tabela
    return fundamentos

# Garantir consistência das colunas
def filtrar_empresas_consistentes(fundamentos, empresas):
    colunas_referencia = list(fundamentos['ABEV3'].columns)
    empresas_consistentes = []

    for empresa in empresas:
        if set(colunas_referencia) == set(fundamentos[empresa].columns):
            empresas_consistentes.append(empresa)
        else:
            fundamentos.pop(empresa)
    
    return fundamentos, empresas_consistentes

# Ajustar colunas duplicadas
def ajustar_colunas_duplicadas(fundamentos):
    exemplo = list(fundamentos.keys())[0]
    colunas_originais = fundamentos[exemplo].columns.tolist()
    texto_colunas = ';'.join(colunas_originais)

    colunas_modificadas = []
    for coluna in colunas_originais:
        if colunas_originais.count(coluna) == 2 and coluna not in colunas_modificadas:
            texto_colunas = texto_colunas.replace(';' + coluna + ';', ';' + coluna + '_1;', 1)
            colunas_modificadas.append(coluna)

    colunas = texto_colunas.split(';')

    for empresa in fundamentos:
        n_colunas = len(fundamentos[empresa].columns)
        fundamentos[empresa].columns = colunas[:n_colunas]

    return fundamentos
