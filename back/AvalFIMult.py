# =============================================================================
""" 1 - Carga Inicial.
"""
# =============================================================================
import os, sys, json
import pickle

from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from flask import redirect, request, Flask, jsonify, make_response

from schemas import AvalFIMultSchema
from urllib.parse import unquote

from logger import setup_logger

# ===============================================================================
""" 2 - Inicializa variáveis de Informações gerais de identificação do serviço.
"""
#  ==============================================================================
info = Info(title="API AvalFIMult", version="1.0.0")
app = OpenAPI(__name__, info=info)

home_tag = Tag(name="Documentação", description="Apresentação da documentação via Swagger.")
obra_tag = Tag(name="Rota em AvalFIMult", description="Avaliação de Viabilidade de Investimento em Fundos Multimercado")
doc_tag = Tag(name="Rota em AvalFIMult", description="Documentação da API tradutor no github")

# ==============================================================================
""" 3 - Inicializa "service_name" para fins de geração de arquivo de log.
"""
# ==============================================================================
service_name = "AvalFIMult"
logger = setup_logger(service_name)

# ==============================================================================
""" 4 - Configurações de "Cross-Origin Resource Sharing" (CORS).
# Foi colocado "supports_credentials=False" para evitar possíveis conflitos com
# algum tipo de configuração de browser. Mas não é a melhor recomendação por 
# segurança. Para melhorar a segurança desta API, o mais indicado segue nas 
# linhas abaixo comentadas.
#> origins_permitidas = ["Obras de Arte"]
#> Configurando o CORS com suporte a credenciais
#> CORS(app, origins=origins_permitidas, supports_credentials=True)
#> CORS(app, supports_credentials=True, expose_headers=["Authorization"])
#> Adicionalmente utilizar da biblioteca PyJWT
"""
# ==============================================================================
CORS(app, supports_credentials=False)

# ================================================================================
""" 5.1 - DOCUMENTAÇÂO: Rota "/" para geração da documentação via Swagger.
"""
# ================================================================================
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger.
    """
    return redirect('/openapi/swagger')

# ================================================================================
""" 5.2 - DOCUMENTAÇÂO: Rota "/doc" para documentação via github.
"""
# ================================================================================
@app.get('/doc', tags=[doc_tag])
def doc():
    """Redireciona para documentação no github.
    """
    return redirect('https://github.com/Moriblo/PUC_EngSoft_MVP4')

# ==============================================================================++
""" 6 - Rota "/AvalFIMult" para tratar o fetch de `GET`.
"""
# ==============================================================================++
@app.get('/AvalFIMult', tags=[obra_tag])

def AvalFIMult():
    """Avaliação de Viabilidade de Investimento em Fundos Multimercado.
    """
    # Lê os valores
    resgate = request.args.get('resgate')
    capta = request.args.get('capta')
    cotistas = request.args.get('cotistas')
    patliq = request.args.get('patliq')
    quota = request.args.get('quota')

    # Lê identificação da origem da solicitação de uso desta API
    origin = request.headers.get('X-Origin')

    # Verifica se o parâmetro 'entrada' foi fornecido
    if not resgate or not capta or not cotistas or not patliq or not quota:
        mesage = f"{resgate},{capta},{cotistas},{patliq},{quota}"
        # mesage = "Erro: Todos os dados devem ser fornecidos!"
        print(mesage)
        return mesage
    else:
        if not origin:
            mesage = "Erro: Sem identificação da origem da chamada!"
            print(mesage)
            return mesage

        path_pkl = "../modelos_ML/"
        modelo_pkl = "FIMulti_SVM_V1.pkl"
        pathmodel = path_pkl + modelo_pkl
        with open(pathmodel, "rb") as f:
            model = pickle.load(f)

        
        # Tratando as variáveis para adequar ao que o modelo espera
        resgate = float(resgate)
        capta = float(capta)
        cotistas = float(cotistas)
        patliq = float(patliq)
        quota = float(quota)

        # Fazer a avaliação para o fundo de investimento com o modelo
        sugest = model.predict([[resgate, capta, cotistas, patliq, quota]])

        # Converter a sugestão em uma string
        sugest_str = str(sugest[0])

        # Retornar com SUGESTÃO (Viável ou Inviável) para a aplicação no fundo de investimento
        print(origin)
        print("A avaliação quanto aos dados do FI é:" + sugest_str)
        return sugest_str


# ===============================================================================
""" 7 - Garante a disponibilidade da API em "suspenso".
"""
# ===============================================================================
if __name__ == '__main__':
    app.run(port=5001, debug=True)