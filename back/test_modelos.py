from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros 
# url_dados = "https://github.com/Moriblo/PUC_EngSoft_MVP4/blob/PyTest/Dataset/goldendata.csv"
url_dados = "https://drive.google.com/file/d/1D0rDXR1xTjGU5XekEAN3ZHnlg6RvX_ul/view?usp=sharing"
colunas = ['RESG_DIA', 'CAPTC_DIA', 'VL_PATRIM_LIQ', 'VL_TOTAL', 'SUGESTÃO']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

# Separando em dados de entrada e saída
X = dataset.iloc[:, 0:-1]
Y = dataset.iloc[:, -1]

# Método para testar o modelo Classification And Regression Trees (CART)
def test_modelo_cart():
    # Importando o modelo
    path_pkl = "../modelos_ML/"
    modelo_pkl = "Pkl_Model_FIMulti_CART.pkl"
    # scaler_pkl = "Pkl_Scaler_Standard.pkl"
    pathmodel = path_pkl + modelo_pkl
    # pathscaler = path_pkl + scaler_pkl
    modelo_cart = Model.carrega_modelo(pathmodel)

    # Obtendo as métricas da Regressão Logística
    acuracia_cart, recall_cart, precisao_cart, f1_cart = avaliador.avaliar(modelo_cart, X, Y)

    # Testando as métricas
    assert acuracia_cart >= 0.5
    assert recall_cart >= 0.5
    assert precisao_cart >= 0.7 
    assert f1_cart >= 0.5 