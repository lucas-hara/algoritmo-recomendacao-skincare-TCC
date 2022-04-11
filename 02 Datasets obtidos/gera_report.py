''' 
Código para criar um relatório contendo as informações dos produtos.

Algoritmo desenvolvido por Lucas Rafael Hara Motta
para o Trabalho de Conclusão do Curso de Inteligência 
Artificial e Aprendizado de Máquina da PUC-MG.
'''

import pandas as pd
from pandas_profiling import ProfileReport

# Leitura do dataset coletado
df = pd.read_csv("Products Info.csv", sep='|')

# Geração do relatório
profile = ProfileReport(df, title="Products Info Report")
profile.to_file("Products Info Report.html")