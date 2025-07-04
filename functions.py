import joblib
import numpy as np

model_all = joblib.load('./models/all.pkl')
model_only_niveis = joblib.load('./models/only_niveis.pkl')
model_only_chuva = joblib.load('./models/only_chuva.pkl')
model_only_itu = joblib.load('./models/only_itu.pkl')
model_only_taio = joblib.load('./models/only_taio.pkl')
import numpy as np
import math

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