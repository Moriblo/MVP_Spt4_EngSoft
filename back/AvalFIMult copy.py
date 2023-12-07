# =============================================================================
""" 1 - Carga Inicial.
"""
# =============================================================================
import os, sys, json
import pickle
import pandas as pd
import numpy as np
import sklearn
import logging

from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from flask import redirect, request, Flask, jsonify, make_response

from urllib.parse import unquote

from sklearn.preprocessing import StandardScaler, MinMaxScaler

from logger import configure_logger
from schemas import FIMulti_schema, error

# ===============================================================================
""" 2 - Inicializa variáveis de Informações gerais de identificação do serviço.
"""
#  ==============================================================================
service_name = "avalfimult"

info = Info(title="API AvalFIMult", version="1.0.0")
app = OpenAPI(__name__, info=info)

home_tag = Tag(name="Documentação", description="Apresentação da documentação.")
obra_tag = Tag(name="Rota em AvalFIMult", description="Avaliação de Viabilidade de Investimento em Fundos Multimercado.")
doc_tag = Tag(name="Rota em AvalFIMult", description="Documentação da API.")

# ==============================================================================
""" 3 - Chama configure_logger para definir "logger.py".
    Os logs podem ser de: info, debug, warning, error ou critical.
""" 
# ==============================================================================
log_path = "log/"
logger = configure_logger(service_name, log_path)

logger.info("*** API avalia fundo de investimento multimercado ***")

# ==============================================================================
""" 4 - Configurações de "Cross-Origin Resource Sharing" (CORS).
# Foi colocado "supports_credentials=False" para evitar possíveis conflitos com
# algum tipo de configuração de browser. Mas não é a melhor recomendação por 
# segurança. Para melhorar a segurança desta API, o mais indicado segue nas 
# linhas abaixo comentadas.
#> origins_permitidas = ["FIMulti"]
#> Configurando o CORS com suporte a credenciais
#> CORS(app, origins=origins_permitidas, supports_credentials=True)
#> CORS(app, supports_credentials=True, expose_headers=["Authorization"])
#> Adicionalmente utilizar da biblioteca PyJWT
"""
# ==============================================================================
# app = Flask(__name__)
CORS(app, supports_credentials=False)

# ================================================================================
""" 5.1 - DOCUMENTAÇÂO: Rota "/" para escolha na geração da documentação.
"""
# ================================================================================
@app.get('/', tags=[home_tag])

def home():
    """Redireciona para /openapi.
    """
    return redirect('/openapi')

# ==============================================================================++
""" 6 - Rota "/avalfimult" para tratar o fetch de `GET`.
"""
# ==============================================================================++
@app.get('/avalfimult', tags=[obra_tag], responses={"200": FIMulti_schema.FIMultiSaidaSchema, "404": error.ErrorSchema})

def avalfimult(query: FIMulti_schema.FIMultiEntradaSchema):
    """Avaliação de Viabilidade de Investimento em Fundos Multimercado.
    """

    resgate = request.args.get('resgate')
    capta = request.args.get('capta')
    patliq = request.args.get('patliq')
    pattotal = request.args.get('pattotal')

    # Verifica se os argumentos recebidos são válidos
    if not all(arg is not None and arg.replace('.', '', 1).isdigit() \
        for arg in [resgate, capta, patliq, pattotal]):
        message = "Os argumentos 'resgate', 'capta', 'patliq' e 'pattotal' \
            recebidos ou estão vazios ou não são números."
        logger.critical(message)
        return message, 400

    # Verifica se o parâmetro 'entrada' foi fornecido
    if resgate is None or capta is None or patliq is None or pattotal is None:
        message = f"Erro: Parâmetros incompletos - resgate: {resgate}, capta: {capta}, \
            patliq: {patliq}, pattotal: {pattotal}"
        logger.critical(message)
        return message
    else:
        # Lê identificação da origem da solicitação de uso desta API
        # origin = request.headers.get('X-Origin')
        # if not origin:
            # message = "Erro: Sem identificação da origem da chamada!"
            # logger.critical(message)

        resgate = float(resgate)
        capta = float(capta)
        patliq = float(patliq)
        pattotal = float(pattotal)

        if patliq < 1000000:
            message = "Erro: patliq deve ser >= 1M !!!"
            logger.error(message)
            return message
        path_pkl = "../modelos_ML/"
        modelo_pkl = "Pkl_Model_FIMulti_CART.pkl"
        scaler_pkl = "Pkl_Scaler_Standard.pkl"
        pathmodel = path_pkl + modelo_pkl
        pathscaler = path_pkl + scaler_pkl

        with open(pathmodel, "rb") as f:
            model = pickle.load(f)
        with open(pathscaler, "rb") as s:
            scaler = pickle.load(s)

        # Estabelece o vetor com os dados informados
        x_entrada = [[resgate, capta, patliq, pattotal]]
        entrada = scaler.transform(x_entrada) # Aplica a formatação do scaler no vetor

        # Aplica o modelo para os valores informados
        sugest = model.predict(entrada)

        # Converter o resultado (sugestão) em uma string
        sugest_str = str(sugest[0])
        if sugest_str != "0" and sugest_str != "1":
            message = "Erro: Nenhum resultado foi obtido!!!" + sugest_str
            logger.error(message)
            return message
        elif sugest_str == "0":
            resultado = "Inviável"
        elif sugest_str == "1":
            resultado = "Viável"
        message = "Resultado: " + resultado

        # Retornar com SUGESTÃO (Viável ou Inviável) para a aplicação no fundo de investimento
        logger.info("Modelo utilizado: " + str(model))
        logger.info("Formato utilizado: " + str(scaler))
        logger.info("Valores recebidos: " + "resgate:" + str(resgate) + "captação:" + str(capta) + \
            "Patrim. Liq.:" + str(patliq) + "Patrim. Total:" + str(pattotal))
        logger.info("Valores convertidos: " + str(entrada))
        logger.info(message + " " + sugest_str)

        return sugest_str


# ===============================================================================
""" 7 - Garante a disponibilidade da API em "suspenso".
"""
# ===============================================================================
if __name__ == '__main__':
    app.run(port=5001, debug=True)