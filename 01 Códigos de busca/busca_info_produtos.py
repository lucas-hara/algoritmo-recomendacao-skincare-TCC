''' 
Código para busca das informações dos produtos.

Algoritmo desenvolvido por Lucas Rafael Hara Motta
para o Trabalho de Conclusão do Curso de Inteligência 
Artificial e Aprendizado de Máquina da PUC-MG.
'''

# Importa as bibliotecas
import json
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Definição do driver de busca
driver = webdriver.Edge("msedgedriver.exe")


# Abre o arquivo json para obter as URLs
with open('../02 Datasets obtidos/Products URLs.json', 'r') as f:
    products_urls = json.load(f)

# Base de dados das informações dos produtos
products_info = []

# Variável para cálculo de tempo
t0_total = time.time()

# Busca as informações dos produtos
for category, urls in products_urls.items():

    # Variável para cálculo de tempo
    t_cat = time.time()

    print(f"Categoria '{category}': {len(products_urls[category])} itens.")

    for idx, url in enumerate(urls[:]):

        # Variável para cálculo de tempo
        t_item = time.time()

        # Busca a URL
        driver.get(url)

        # Verifica se a página foi carregada (timeout = 30s)
        element_present = EC.presence_of_element_located(
            (By.CLASS_NAME, 'product-reviews-header'))
        WebDriverWait(driver, 30).until(element_present)

        # Variável de informações do produto
        product = {}
        product = {
            "Brand": driver.find_element(by=By.CLASS_NAME, value='product-brand').text,
            "Name": driver.find_element(by=By.CLASS_NAME, value='product-heading').text,
            "Rating": None,
            "Price": None,
            "Product URL": url,
            "Image URL": None,
            "Category": category.replace("-", " ").title(),
            # "Skin Type": None,
            # "Skin Concerns": None,
            # "Formulation": None,
            # "Skincare By Age": None,
            # "Ingredients": None
        }

        # Encontra o valor de avaliação (se existir)
        try:
            product['Rating'] = driver.find_element(
                by=By.CLASS_NAME, value='product-rating-text').text
        except:
            product['Rating'] = None

        # Encontra o valor de preço
        price_fields = driver.find_elements(
            by=By.CLASS_NAME, value='product-price')
        for field in price_fields:
            if field.text != "":
                product['Price'] = field.text

        # Encontra a URL da imagem
        image = driver.find_element(
            by=By.CLASS_NAME, value='variant-image-border-space')
        product['Image URL'] = image.get_attribute('src')

        # Encontra e formata o campo 'DESCRIPTION' (se existir)
        # (Fornece principalmente os dados: 'Skin Type', 'Skin Concerns', 'Formulation' e 'Skincare by Age')
        try:
            description = driver.find_element(
                by=By.CLASS_NAME, value='product-filter-types-values').text
            for item in description.split("\n"):
                label, values = item.split(": ")
                product[label] = values
        except:
            pass

        # Encontra o valor de ingredientes (se existir)
        try:
            # Clica no botão para mostrar informações dos ingredientes e busca a lista de ingredientes
            driver.find_elements(
                by=By.CLASS_NAME, value='read-more-button')[1].click()
            product['Ingredients'] = driver.find_element(
                by=By.CLASS_NAME, value='product-ingredients-values').text
        except:
            product['Ingredients'] = None

        # Adiciona as informações do produto na lista de produtos
        products_info.append(product)

        # Mostra acompanhamento da busca (item)
        print(
            f"Item {idx+1}/{len(urls)} ({(time.time()-t_item):.2f}s): {product['Name']}")

    # # Salva as informações em um arquivo csv por categoria
    # df_cat = pd.DataFrame(products_info)
    # df_cat.to_csv(
    #     f"../02 Datasets obtidos/Products Info_{category}.csv", sep="|", index=False)

    # Mostra acompanhamento da busca (categoria)
    print(f"Categoria {category} completa! ({(time.time()-t_cat):.2f}s) \n")


# Salva os links em um arquivo csv
df = pd.DataFrame(products_info)
df.to_csv("../02 Datasets obtidos/Products Info.csv", sep="|", index=False)

# Mostra o resultado
print(df.head()+"\n")
print(df.info())

print(f"Código executado em {(time.time()-t0_total):.2f}s. \n")
