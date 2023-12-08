from sklearn.tree import DecisionTreeClassifier
from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros
url = "../Dataset/goldendata.csv"
atributos = ['RESG_DIA', 'CAPTC_DIA', 'VL_PATRIM_LIQ', 'VL_TOTAL', 'SUGESTÃO']

# Carga dos dados
dataset = carregador.carregar_dados(url)
# Coleta a quantidade de linhas do dataset para que seja usado na aplição do modelo
qtde_lines = dataset.shape[0]

# Separando em dados de entrada e saída
X = dataset.iloc[:, 0:-1]
X_columns = dataset.iloc[:, 0:-1].columns.tolist()

Y = dataset.iloc[:, -1]
Y_column = dataset.columns[-1]

# Método para testar o modelo Classification And Regression Trees (CART)
def test_modelo_cart():
    # Importando o modelo
    path_pkl = "../modelos_ML/"
    modelo_pkl = "Pkl_Model_FIMulti_CART.pkl"
    scaler_pkl = "Pkl_Scaler_Standard.pkl"
    pathmodel = path_pkl + modelo_pkl
    pathscaler = path_pkl + scaler_pkl

    # Carregando o modelo e o scaler
    modelo_cart, scaler_cart = modelo.carrega_modelo(pathmodel, pathscaler)
    params = modelo_cart.get_params()
    expected_params = {'max_depth': 15, 'min_samples_leaf': 2, 'min_samples_split': 5}

    # Obtendo os resultados da aplicação do modelo
    acuracia_cart, precisao_cart_1, precisao_cart_0 = avaliador.avaliar(dataset, qtde_lines, atributos, \
        modelo_cart, scaler_cart)

    """
    Verificando a coleta dos dados, consistência dos atributos, do modelo carregado, 
    dos parâmetros do modelo, e por fim das expectativas de acurácia e precisão para o modelo.
    """
    assert not dataset.empty, "O DataFrame está vazio"
    assert X_columns == ['RESG_DIA', 'CAPTC_DIA', 'VL_PATRIM_LIQ', 'VL_TOTAL'], "As colunas em X não correspondem"
    assert Y_column == 'SUGESTÃO', "A coluna em Y não corresponde"
    assert isinstance(modelo_cart, DecisionTreeClassifier), "Não é o modelo esperado"
    for param, value in expected_params.items():
        assert params[param] == value, f"Valor inesperado para {param}: obtido {params[param]}, esperado {value}"

    """
    O objetivo foi balancear os resultados de acurácia com o de precisão, considerando a precisão 
    para a classe 1 como mais crítica. Entende-se que, apontar um falso positivo para a viabilidade 
    de um investimento, é mais crítico do que inviabilizar um investimento. Ou seja, um falso 
    positivo pode levar a comprometimento de recurso financeiro.
    """
    assert acuracia_cart >= 0.65, "Índice de acurácia abaixo do limiar"
    assert precisao_cart_1 >= 0.75, "Índice para classe 1, crítico para heurística de negócio,\
         abaixo do limiar"
    assert precisao_cart_0 >= 0.1, "Índice para classe 0 abaixo do limiar"