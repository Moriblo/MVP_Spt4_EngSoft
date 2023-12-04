from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.metrics import precision_recall_fscore_support
import pandas as pd

class Avaliador:

    def avaliar(self, dataset, qtde_lines, atributos, modelo, scaler):
        """ A partir dos dados do golden data, aplica o modelo e restorna os resultados do 
        classification report
        """
        SUGESTÃO_CALC = []

        df_carga = list(dataset[atributos].sample(qtde_lines).itertuples(index=False, name=None))

        carga_entrada = pd.DataFrame([tupla[:4] for tupla in df_carga], columns=atributos[:4])
        carga_saida = pd.DataFrame([tupla[4] for tupla in df_carga], columns=[atributos[-1]])

        array_entrada = carga_entrada.values

        X_entrada = array_entrada[:,0:4].astype(float)
        rescaledEntradaX = scaler.transform(X_entrada)

        for i in range(qtde_lines):
            resultado = modelo.predict(rescaledEntradaX)

        SUGESTÃO_CALC.extend(resultado)

        # Obtendo os resultado da aplicação do modelo
        acuracia = accuracy_score(carga_saida, SUGESTÃO_CALC)
        precisao, recall, fscore, suporte = precision_recall_fscore_support(carga_saida, SUGESTÃO_CALC)

        precisao_1 = precisao[1]

        return acuracia, precisao_1
