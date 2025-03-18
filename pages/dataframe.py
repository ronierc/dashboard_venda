import streamlit as st
from dataset import df
from utils import convert_csv, mensagem_sucesso

st.title('Dataset de Vendas')
with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas',
        list(df.columns),
        list(df.columns)
    )
st.sidebar.title('Filtros')
with st.sidebar.expander('Categoria do Produto'):
    categorias = st.multiselect(
        'Selecione as Categorias',
        df['Categoria do Produto'].unique(),
        df['Categoria do Produto'].unique()
    )
with st.sidebar.expander('Preço do Produto'):
    preco = st.slider(
        'Selecione as Preço',
        int(df['Preço'].min()), int(df['Preço'].max()),
        (int(df['Preço'].min()),int(df['Preço'].max()))
    )
with st.sidebar.expander('Data da Compra'):
    data_compra = st.date_input(
        'Selecione a Data',
        (df['Data da Compra'].min(), df['Data da Compra'].max())
    )

# Lógica para garantir que data_fim seja igual a data_inicio se apenas uma data for selecionada
if len(data_compra) == 1:
    data_compra = (data_compra[0], data_compra[0])  # Se uma data for escolhida, ajusta data_fim para ser igual a data_inicio
else:
    data_compra = (data_compra[0], data_compra[1])  # Caso contrário, mantém o intervalo de datas selecionado


query = '''
    `Categoria do Produto` in @categorias and \
    @preco[0] <= Preço <= @preco[1] and \
    @data_compra[0] <= `Data da Compra` <= @data_compra[1]
'''

filtro_dados = df.query(query)
filtro_dados = filtro_dados[colunas]


st.dataframe(filtro_dados)

st.markdown(f'A tabela possui :blue[{filtro_dados.shape[0]}] linhas e :blue[{filtro_dados.shape[1]}] colunas')

st.markdown('Escreva um nome do Arquivo')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input(
        '',
        label_visibility='collapsed'
    )
    nome_arquivo += '.csv'
with coluna2:
    st.download_button(
        'Baixar Arquivo',
        data=convert_csv(filtro_dados),
        file_name=nome_arquivo,
        mime='text/csv',
        on_click=mensagem_sucesso
    )