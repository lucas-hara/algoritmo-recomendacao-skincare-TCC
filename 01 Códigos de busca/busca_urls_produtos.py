''' 
Código para busca das URLs dos produtos.

Algoritmo desenvolvido por Lucas Rafael Hara Motta
para o Trabalho de Conclusão do Curso de Inteligência 
Artificial e Aprendizado de Máquina da PUC-MG.
'''

# Importa as bibliotecas
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Definição da URL principal, categorias e conversão (RM para USD)
url = "https://www.sephora.my/categories/skincare"
categories = ['cleanser-and-exfoliator', 'toner', 'moisturiser',
              'masks-and-treatments', 'suncare']

# Definição do driver de busca
driver = webdriver.Edge("msedgedriver.exe")

# Banco de dados de URLs dos produtos
product_urls = {}

# Variável para cálculo de tempo
t0_total = time.time()

# Obtenção das URLs de todas as páginas de todas as categorias
for category in categories:

    # Lista com URLs das categorias
    categories_urls = []

    # Abre a página da categoria e verifica se ela foi carregada (timeout=20s)
    driver.get(f"{url}/{category}")

    element_present = EC.presence_of_element_located(
        (By.CLASS_NAME, 'pagination'))
    WebDriverWait(driver, 20).until(element_present)

    # Encontra a última página da categoria
    last_page = int(driver.find_elements_by_class_name('page')[-2].text)

    for page in range(1, last_page+1):

        print(f"Buscando em '{category}', pág. {page}.")

        # Variável para cálculo de tempo
        t0 = time.time()

        # Busca a URL
        driver.get(f"{url}/{category}?page={page}")

        # Verifica se a página foi carregada (timeout = 10s)
        element_present = EC.presence_of_element_located(
            (By.CLASS_NAME, 'pagination'))
        WebDriverWait(driver, 10).until(element_present)

        # Captura elementos relacionados aos produtos
        elements = driver.find_elements_by_class_name(
            "product-card-image-container")

        for elem in elements:
            categories_urls.append(elem.get_attribute('href'))

        print(
            f"Encontrado {len(elements)} elementos em {(time.time()-t0):.2f}s. \n")

    product_urls[category] = categories_urls
    print(f"Categoria '{category}': busca completa. \n")

# Salva os links em um arquivo json
with open('../02 Datasets obtidos/Products URLs.json', 'w') as f:
    json.dump(product_urls, f)

# Mostra o resultado
print("CATEGORIA".ljust(30) + "QTD. ITENS")
for key, value in product_urls.items():
    print(key.ljust(30) + str(len(value)))

# Verifica o tempo de execução
print(f"Código executado em {(time.time()-t0_total):.2f}s. \n")
