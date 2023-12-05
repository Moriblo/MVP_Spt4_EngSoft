MVP da Sprint 4 da Pós Graduação em Engenharia de Software
# Esquema básico de um Projeto de Ciência de Dados
![Esquema básico de um Projeto de Ciência de Dados](https://github.com/Moriblo/PUC_EngSoft_MVP4/blob/main/images/Esquema%20B%C3%A1sico%20de%20um%20Projeto%20de%20Ci%C3%AAncia%20de%20Dados.png)

* ## Definição do Problema
  Estabelecer uma forma simples de avaliação de viabilidade de um fundo de investimentos, com um nível razoável de assertividade, considerando um número mínimo de variáveis. Entendendo como viabilidade, o aumento do valor da quota, em um período de carência de 30 (trinta) dias corridos.

  :warning: ***Note que aqui não se fala de rendimento, mas sim se a variação da quota foi positiva no período.***

* ## Coleta e Análise de Dados
  São utilizados dados diários dos fundos cadastrados na Comissão de Valores Mobiliários (CVM). _Por conta dos tamanhos das bases utilizadas (dois meses com dados de performance diária para o treinamento do modelo, dois outros meses para a geração do golden data, e mais a base de cadastro dos fundos), não foi possível a manipulação destas no github, **utilizando-se do google drive. O diretório está compartilhado para "qualquer pessoa com o link"**_.

  🔗 Fonte dos dados: https://dados.cvm.gov.br/dataset/fi-doc-inf_diario <br>
  🔗 Link do google drive: https://drive.google.com/drive/folders/1bBSueloNniaey8LpJzwfipWTuS1sn9LR?usp=sharing

* ## Pré-processamento
  ***Restrições:***
  
  1 - Valor da quota [VL_QUOTA] > 0 por entender que um fundo com valor de quota negativo, já é um fundo "esgotado" que não deve estar na base de análise.

  2 - Número de Cotistas [NR_COTST] > 15.000 por avaliar, durante análises dos dados dos datasets, que valores menores afetavam significativamente o comportamento de resgates e captações diárias.

  3 - Valor do Patrimônio Líquido [VL_PATRIM_LIQ] > 1.000.000 por avaliar, durante análises dos dados dos datasets, que valores menores afetavam significativamente o comportamento de resgates e captações diárias.

  4 - Classe do Fundo [CLASSE] = Fundo Multimercado, por ser um fundo de investimento de perfil intermediário, não tão conservador quanto um Fundo de Renda Fixa, nem tão arrojado quanto um Fundo de Ações. Todos os demais fundos constantes nos datasets (Fundo de Curto Prazo, Fundo Cambial, Fundo Referenciado, Fundo da Dívida Externa e FMP-FGTS), são fundos de classes muito específicas.

  ***Feature Selection and Engineering:***
  
  ATRIBUTO ALVO:: RET_VL_QUOTA = VL_QUOTA (M+1) - VL_QUOTA (M). Se RET_VL_QUOTA > 0, SUGESTÃO = 1, investimento VIÁVEL, caso contrário SUGESTÃO = 0, INVIÁVEL. O atributo alvo é o campo [SUGESTÃO].

  FEATURES:: Foram pré-selecionadas 7 (sete) colunas das 10 (dez) originais.

  ***OBS*** - Foram utilizados os meses 9/23 e 10/23 para geração das bases de treino e teste. Foram utilizados os meses 7/23 e 8/23 para geração da base de simulação.

* ## Modelagem e Inferência
* ## Pós-processamento
* ## Apresentação de Resultados
* ## Implantação do Modelo e Geração de Valor
