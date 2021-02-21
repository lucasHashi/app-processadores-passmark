import streamlit as st
import pandas as pd


URL_PASSMARK_PROCESSADORES = 'https://www.cpubenchmark.net/cpu_list.php'

PROCESSADORES_AMD = ['Athlon', 'Ryzen', 'PRO', 'Opteron', 'Phenom', 'Turion', 'AMD']
PROCESSADORES_INTEL = ['Xeon', 'Pentium', 'Core', 'Atom', 'Celeron']

DOLAR_HOJE = 5.4


def main():
    df_processadores = carregar_dados_excel()

    st.title('Analise de processadores e pontuações')
    st.write('# Pesquisa dos seu processador atual')

    meu_processador = st.text_input('Nome do processador')

    st.write(
        df_processadores[df_processadores['processador'].str.contains(meu_processador)]
    )


    st.write('# Filtro pelos mais custo-benefício')

    moeda_escolhida = st.selectbox('Moeda para analisar o preço', ['Reais', 'Dolares'], 0) # 'dolares' ou 'reais'
    if moeda_escolhida == 'dolares':
        coluna_custo_beneficio = 'custo_beneficio_dol'
    else:
        coluna_custo_beneficio = 'custo_beneficio_reais'
    
    pontuacao_minima_escolhida = st.slider('Pontuação mínima', 0, int(df_processadores['pontuacao'].max()))
    custo_beneficio_minimo_escolhido = st.slider('Custo-benefício mínimo', 0.0, df_processadores[coluna_custo_beneficio].max())

    lista_fabricantes = list(df_processadores[~df_processadores['fabricante'].isna()]['fabricante'].unique())
    lista_fabricantes.sort()
    lista_fabricantes.insert(0, 'Todos')
    fabricante_escolhido = st.selectbox('Fabricante do processador', lista_fabricantes)

    if fabricante_escolhido == 'Todos':
        lista_modelos = df_processadores[
            ~df_processadores['fabricante'].isna()
        ]['modelo'].unique()
    else:
        lista_modelos = df_processadores[
            (~df_processadores['fabricante'].isna()) &
            (df_processadores['fabricante'] == fabricante_escolhido)
        ]['modelo'].unique()
    
    lista_modelos = list(lista_modelos)
    lista_modelos.sort()
    lista_modelos.insert(0, 'Todos')
    modelo_escolhido = st.multiselect('Modelos de processador', lista_modelos)

    quant_itens_trazer = st.slider('Quantos processadores trazer', 1, 25, 10)

    df_melhores_processadores = df_processadores[
        (df_processadores['pontuacao'] > pontuacao_minima_escolhida) &
        (df_processadores[coluna_custo_beneficio] > custo_beneficio_minimo_escolhido)
    ]


    if not fabricante_escolhido == 'Todos':
        df_melhores_processadores = df_processadores[
            df_processadores['fabricante'] == fabricante_escolhido
        ]
    
    if not 'Todos' in modelo_escolhido:
        df_melhores_processadores = df_processadores[
            df_processadores['modelo'].isin(modelo_escolhido)
        ]

    st.table(
        df_melhores_processadores\
        .sort_values(coluna_custo_beneficio, ascending=False)\
        .dropna()\
        .head(quant_itens_trazer)\
        .reset_index(drop=True)\
        .drop(['rank', 'modelo', 'fabricante'], axis=1)
    )


    st.write('## Ultimos lugares')

    st.table(
        df_melhores_processadores\
        .sort_values(coluna_custo_beneficio, ascending=True)\
        .dropna()\
        .head(5)\
        .reset_index(drop=True)\
        .drop(['rank', 'modelo', 'fabricante'], axis=1)
    )


@st.cache
def carregar_dados_excel():
    df_processadores = pd.read_pickle('dados_processados_processadores.pickle')

    return df_processadores


if __name__ == '__main__':
    main()