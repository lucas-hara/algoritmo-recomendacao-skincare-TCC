import streamlit as st
import numpy as np
import pandas as pd

print("\n\nSTARTING....")

# Configura página
st.set_page_config(
    page_title="Recomendação de produtos de skincare",
    page_icon='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/310/lotion-bottle_1f9f4.png'
)


@st.cache
# Função para carregamento da matriz de similaridade e do dataset
def load_data():
    sim_matrix = np.load(
        "03 Notebook e datasets gerados/Similarity Matrix.npy")
    df = pd.read_csv(
        "03 Notebook e datasets gerados/Exploded Dataframe.csv")

    # Remove os itens do formato de lista para determinadas colunas
    for col in ["Skin Type", "Skin Concerns", "Formulation", "Skincare By Age", "Ingredients", "Function"]:
        df[col] = df[col].apply(
            lambda x: ", ".join(eval(x))
        )

    return sim_matrix, df


# Criação do algoritmo de busca dos produtos similares
def busca_similares(id_produto, sim_matrix):

    # Encontra os valores similares do produto indicado, colocando em ordem decrescente
    similar_list = list(enumerate(sim_matrix[id_produto][0]))
    sorted_similar_list = sorted(
        similar_list, key=lambda x: x[1], reverse=True)

    # Seleciona os 5 produtos mais similares (além do próprio produto)
    top_5 = sorted_similar_list[0:6]

    # Retorna a lista com os índices e valores de similaridade dos 5 produtos mais semelhantes
    top_5_idx, top_5_values = zip(*top_5)

    # Cria um dataframe com os 5 produtos mais semelhantes, baseado no dataframe original
    df_top_5 = df.iloc[list(top_5_idx)].copy()
    df_top_5['Similarity'] = [f"{(100*x).round(1)}%" for x in top_5_values]

    return df_top_5


# Função para a criação de uma matriz resumida
def get_resumed_df(df):
    df_resumed = pd.DataFrame()
    df_resumed['Full Name'] = df['Full Name']
    for col in df.drop('Full Name', axis=1):
        df_resumed[col] = df[col]

    df_resumed.drop(["Brand", "Name", "Product URL",
                    "Image URL"], axis=1, inplace=True)

    return df_resumed


# Carrega dados
sim_matrix, df = load_data()

# Cria layout da página
st.write("# Recomendação de produtos de skincare")
st.caption("Este aplicativo foi desenvolvido por Lucas Rafael Hara Motta para o curso de Inteligência Artificial e Machine Learning da PUC-MG.")
st.caption(
    "Todos os produtos, informações e imagens foram obtidos do site [Sephora Malaysia](https://www.sephora.my/).")
st.caption(
    "Contato: [Linkedin](https://www.linkedin.com/in/lucashara/) | [GitHub](https://github.com/lucas-hara)")

st.write("### \n### Escolha um produto:")

# Cria caixa de seleção
product = st.selectbox("Produto:", df['Full Name'].sort_values())

prod_id = df[df['Full Name'] == product].index

df_top_5 = busca_similares(prod_id, sim_matrix)
df_resumed = get_resumed_df(df_top_5)

with st.expander("Mais informações..."):
    st.table(df_resumed[:1].T.astype(str))

st.write("### Produtos recomendados:")

# Mostra os produtos recomendados
for idx, (index, row) in enumerate(df_top_5.iterrows()):

    if idx == 0:
        continue

    st.write("#### ━━━")

    # Definição das colunas
    col1, col2, col3 = st.columns([0.1, 0.3, 0.7])

    # Coluna 1: ranking
    col1.metric("Rank", idx)

    # Coluna 2: imagem do produto
    col2.image(row["Image URL"])

    # Coluna 3: Informações do produto
    with col3.container():

        st.write(f'''
            <p style="bold: True; color: #454545; font-size: 22px;"> 
                <b>{row["Brand"]}</b><br>
                {row["Name"]}

            </p>''', unsafe_allow_html=True)

        st.write(f'''
            <p style="bold: True; color: gray; font-size: 18px;"> 
                Similaridade: {row["Similarity"]}
            </p>''', unsafe_allow_html=True)

        st.caption(f"[LINK DO PRODUTO]({row['Product URL']})")

    with st.expander("Mais informações..."):
        st.table(df_resumed.iloc[idx])
