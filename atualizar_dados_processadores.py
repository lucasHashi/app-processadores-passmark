import pandas as pd



def download_dados_processados():
    df_processadores = pd.read_html(URL_PASSMARK_PROCESSADORES)[0]

    df_processadores.columns = ['processador', 'pontuacao', 'rank', 'custo_beneficio_dol', 'preco_dol']

    # Organizacao do preco em dolar
    df_processadores['preco_dol'] = df_processadores['preco_dol'].str.replace('$', '')
    df_processadores['preco_dol'] = df_processadores['preco_dol'].str.replace('*', '')
    df_processadores['preco_dol'] = df_processadores['preco_dol'].str.replace(',', '')
    df_processadores['preco_dol'] = df_processadores['preco_dol'].astype('float')

    df_processadores.dropna(inplace=True)

    # Calculo dos valores em reais
    df_processadores['preco_reais'] = df_processadores['preco_dol'] * DOLAR_HOJE
    df_processadores['custo_beneficio_reais'] = df_processadores['pontuacao'] / df_processadores['preco_reais']
    df_processadores['custo_beneficio_reais'] = df_processadores['custo_beneficio_reais'].round(2)

    df_processadores.loc[df_processadores['processador'].str.contains('Xeon'), 'modelo'] = 'Xeon'
    df_processadores.loc[df_processadores['processador'].str.contains('Pentium'), 'modelo'] = 'Pentium'
    df_processadores.loc[df_processadores['processador'].str.contains('Core'), 'modelo'] = 'Core'
    df_processadores.loc[df_processadores['processador'].str.contains('Atom'), 'modelo'] = 'Atom'
    df_processadores.loc[df_processadores['processador'].str.contains('Celeron'), 'modelo'] = 'Celeron'

    df_processadores.loc[df_processadores['processador'].str.contains('Athlon'), 'modelo'] = 'Athlon'
    df_processadores.loc[df_processadores['processador'].str.contains('Ryzen'), 'modelo'] = 'Ryzen'
    df_processadores.loc[df_processadores['processador'].str.contains('PRO'), 'modelo'] = 'PRO'
    df_processadores.loc[df_processadores['processador'].str.contains('Phenom'), 'modelo'] = 'Phenom'
    df_processadores.loc[df_processadores['processador'].str.contains('Opteron'), 'modelo'] = 'Opteron'
    df_processadores.loc[df_processadores['processador'].str.contains('Turion'), 'modelo'] = 'Turion'
    df_processadores.loc[df_processadores['processador'].str.contains('AMD'), 'modelo'] = 'AMD'

    df_processadores.loc[df_processadores['modelo'].isin(PROCESSADORES_AMD), 'fabricante'] = 'AMD'
    df_processadores.loc[df_processadores['modelo'].isin(PROCESSADORES_INTEL), 'fabricante'] = 'Intel'

    df_processadores.dropna(inplace=True)

    df_processadores.to_pickle('dados_processados_processadores.pickle')


if __name__ == '__main__':
    main()