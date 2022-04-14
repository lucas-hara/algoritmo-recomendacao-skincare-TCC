# Algoritmo de Recomendação de Skincare
## Desenvolvido por: Lucas Rafael Hara Motta
Este algoritmo foi desenvolvido para o Trabalho de Conclusão do Curso de Inteligência Artificial e Aprendizado de Máquina da PUC-MG.  
O trabalho tem como objetivo criar um algoritmo de recomendação de produtos de skincare a partir da base de dados da Sephora Malásia.  
Todas as informações, produtos e imagens coletados foram obtidos do site [Sephora Malaysia](https://www.sephora.my/).  

Este repositório contempla os códigos para coleta, análise e tratamento dos dados, desenvolvimento do algoritmo de recomendação e criação de um aplicativo com interface para interação do usuário.  

O aplicativo gerado encontra-se na URL: https://share.streamlit.io/lucas-hara/algoritmo-recomendacao-skincare-tcc/main/app.py.

### 01 Códigos de Busca

O algoritmo presente em `busca_urls_produtos.py` foi criado para buscar as URLs de todos os produtos da sessão de skincare do site da Sephora Malásia e armazenar no banco de dados 'Products URLs.json'.  
A partir disso, o código `busca_info_produtos.py` extrai toda a informação relacionada a cada um dos produtos e armazena em um banco de dados no arquivo '02 Datasets obtidos/Products Info.csv'.  
O arquivo `msedgedriver.exe` é um driver que permite a utilização da biblioteca `selenium` no Microsoft Edge.  

### 02 Datasets obtidos

Esta pasta contém os banco de dados coletados na etapa anterior, além de um algoritmo utilizando a biblioteca `pandas-profiling, para gerar um relatório com análise exploratória dos dados, encontrado em `gera_report.py`. Este relatório é mostrado no arquivo 'Products Info Report.html'.

### 03 Notebook e datasets gerados

Esta pasta contempla o notebook `Algoritmo de Recomendação.ipynb`, criado em Jupyter para análise e tratamentos dos dados obtidos.  
Neste mesmo notebook foi desenvolvido o algoritmo de recomendação baseado na similaridade dos ingredientes que compõem cada um dos produtos, além de algumas funcionalidades. Dois arquivos foram salvos para serem utilizados no aplicativo: 
- 'Exploded Dataframe.csv': contém o dataset com as informações tratadas dos produtos;
- 'Similarity Matrix.npy': matriz de similaridade entre os produtos. 

### 04 App

Para facilitar a interação com o algoritmo, um aplicativo foi desenvolvido utilizando a biblioteca `streamlit`. Esta biblioteca permite gerar rapidamente aplicativos para aprendizado de máquina inteiramente em `python`.  
O aplicativo gerado está no arquivo `app.py`, na raiz deste repositório e seu deploy foi realizado na própria plataforma do `streamlit`, podendo ser acessado pela URL: https://share.streamlit.io/lucas-hara/algoritmo-recomendacao-skincare-tcc/main/app.py. 
