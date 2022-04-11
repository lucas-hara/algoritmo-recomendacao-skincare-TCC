from math import prod
import streamlit as st
import numpy as np
import pandas as pd

print("\n\nSTARTING....")

# Configura página
st.set_page_config(
    page_title="Recomendação de produtos de skincare",
    layout='wide',
    #page_icon= 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/304/lotion-bottle_1f9f4.png'
    #page_icon= 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/google/313/lotion-bottle_1f9f4.png'
    page_icon='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/microsoft/310/lotion-bottle_1f9f4.png'
)


@st.cache
def load_data():
    sim_matrix = np.load("Similarity Matrix.npy")
    df = pd.read_csv("Exploded Dataframe.csv")

    df.drop(['Brand', 'Name'], axis=1, inplace=True)
    cols = df.columns.to_list()
    cols.remove("Full Name")
    cols = ["Full Name"] + cols
    df = df[cols]

    return sim_matrix, df


def get_top5(prod_id):
    similar_list = list(enumerate(sim_matrix[prod_id][0]))
    sorted_similar_list = sorted(
        similar_list, key=lambda x: x[1], reverse=True)
    top_5 = sorted_similar_list[0:6]

    top_5_idx, top_5_sim = zip(*top_5)
    top_5_idx = list(top_5_idx)
    top_5_sim = [f"{(100*x):.1f} %" for x in top_5_sim]

    df_top5 = df.iloc[list(top_5_idx)].copy()
    df_top5['Similarity'] = top_5_sim

    return df_top5


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

df_top5 = get_top5(prod_id)

# Mostra os produtos recomendados
for idx, (index, row) in enumerate(df_top5.iterrows()):
    st.write("###")

    if idx == 0:
        continue

    url = "https://image-optimizer-reg.production.sephora-asia.net/images/product_images/closeup_1_Product_9336328011956-Alpha-H-Beauty-Sleep-Power-Peel-50ml_a227bb1064e2bb9d148a3d15d0abd4e654a8cf15_1617778706.png"

    if idx == 1:
        base_delta = float(row['Similarity'].split(" ")[0])
        delta = ""

    else:
        delta_i = float(row['Similarity'].split(" ")[0])
        delta = f"{(delta_i - base_delta):.1f}%"

    col1, col2 = st.columns([1, 4])

    col1.image(url)
    #col1.markdown('<p style="color:Blue; font-size: 20px;">Original image</p>',unsafe_allow_html=True)
    # col2.metric(
    #     label=row['Full Name'],
    #     #label="[Teste](https://www.google.com)",
    #     value=row['Similarity'],
    #     #delta= delta
    # )
    with col2.container():

        st.write(f'''
            <p style="bold: True; color: white; font-size: 22px;"> 
                <b>{row["Full Name"]}</b>
            </p>''', unsafe_allow_html=True)


        st.write(f'''
            <p style="bold: True; color: white; font-size: 30px;"> 
                {row["Similarity"]}
            </p>''', unsafe_allow_html=True)

        # st.write(f'''
        #     <p style="bold: True; color: red; font-size: 30px;"> 
        #         {delta}
        #     </p>''', unsafe_allow_html=True)



        st.caption(f"[LINK]()")
        # st.write(f'''
        #     <p style="bold: True; color: white; font-size: 18px;"> 
        #         <a href="https://www.google.com.br">LINK
        #     </p>''', unsafe_allow_html=True)

    with st.expander("Mais informações..."):
        st.table(row)


def get_link(prod_name):
    prod_name.replace("%", "percent")
    prod_name.replace("|", "")
