import joblib
import numpy as np
import math

model_all = joblib.load('./models/all.pkl')
model_only_niveis = joblib.load('./models/only_niveis.pkl')
model_only_chuva = joblib.load('./models/only_chuva.pkl')
model_only_itu = joblib.load('./models/only_itu.pkl')
model_only_taio = joblib.load('./models/only_taio.pkl')


def forecast(dados: dict):
    def parse_value(key):
        val = dados.get(key)
        if val is None:
            return None
        try:
            val_float = float(val)
            if math.isnan(val_float):
                return None
            return val_float
        except (ValueError, TypeError):
            return None

    rio_itu = parse_value('rio_itu')
    chuva_itu = parse_value('chuva_itu')
    rio_taio = parse_value('rio_taio')
    chuva_taio = parse_value('chuva_taio')

    previsoes = []

    # verifica se os dados são válidos (não None)
    if None not in (rio_itu, chuva_itu, rio_taio, chuva_taio):
        entrada = np.array([[rio_itu, chuva_itu, rio_taio, chuva_taio]])
        previsao = model_all.predict(entrada)[0]
        previsoes.append(["Todos os dados", previsao/100])

    if None not in (rio_itu, rio_taio):
        entrada = np.array([[rio_itu, rio_taio]])
        previsao = model_only_niveis.predict(entrada)[0]
        previsoes.append(["Somente níveis", previsao/100])

    if None not in (chuva_itu, chuva_taio):
        entrada = np.array([[chuva_itu, chuva_taio]])
        previsao = model_only_chuva.predict(entrada)[0]
        previsoes.append(["Somente chuva", previsao/100])

    if None not in (rio_itu, chuva_itu):
        entrada = np.array([[rio_itu, chuva_itu]])
        previsao = model_only_itu.predict(entrada)[0]
        previsoes.append(["Somente Ituporanga", previsao/100])

    if None not in (rio_taio, chuva_taio):
        entrada = np.array([[rio_taio, chuva_taio]])
        previsao = model_only_taio.predict(entrada)[0]
        previsoes.append(["Somente Taió", previsao/100])

    return previsoes


def media_ponderada_modelos(valores: dict) -> float:
    erros_rmse = {
        "todos": 28.92,
        "somente_niveis": 29.06,
        "somente_chuva": 139.58,
        "somente_taio": 48.61,
        "somente_ituporanga": 59.36
    }

    soma_ponderada = 0
    soma_pesos = 0

    for modelo, valor in valores.items():
        erro = erros_rmse.get(modelo)
        if erro is None or erro == 0:
            continue 
        peso = 1 / erro
        soma_ponderada += valor * peso
        soma_pesos += peso

    if soma_pesos == 0:
        raise ValueError("Nenhum modelo válido ou erro zero.")

    return soma_ponderada / soma_pesos

def extrair_equacao(modelo, nomes_variaveis=None):
    if hasattr(modelo, 'coef_') and hasattr(modelo, 'intercept_'):
        coef = modelo.coef_
        intercept = modelo.intercept_
        termos = []

        if nomes_variaveis is None:
            nomes_variaveis = [f'x{i+1}' for i in range(len(coef))]

        for nome, valor in zip(nomes_variaveis, coef):
            termos.append(f'({valor:.4f} * {nome})')

        equacao = ' + '.join(termos)
        equacao += f' + ({intercept:.4f})'
        return f'y = {equacao}'
    else:
        return "Modelo não possui coeficientes acessíveis."

def get_modelo_eq():
    return {
        "todos_os_dados": extrair_equacao(model_all, ['rio_itu', 'chuva_itu', 'rio_taio', 'chuva_taio']) ,
        "somente_níveis": extrair_equacao(model_only_niveis, ['rio_itu', 'rio_taio']),
        "somente_chuva": extrair_equacao(model_only_chuva, ['chuva_itu', 'chuva_taio']),
        "somente_ituporanga": extrair_equacao(model_only_itu, ['rio_itu', 'chuva_itu']),
        "somente_taió":extrair_equacao(model_only_taio, ['rio_taio', 'chuva_taio']) 
    }