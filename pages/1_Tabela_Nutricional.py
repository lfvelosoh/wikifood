import streamlit as st
import sqlite3
import pandas as pd

 
def main():

    st.set_page_config(
        page_title="WikiFood",
        page_icon="🍔",
    )

    st.title('📋 Tabela Nutricional')
    st.write('Consulte a composição nutricional dos alimentos.')
    st.divider()

    conn = sqlite3.connect('dados.db')
    tabela = pd.read_sql_query("SELECT * from tabela", conn)
    conn.close()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Filtro')
        tipo = st.selectbox('Selecione o tipo do alimento', tabela['tipo do alimento'].unique())
        alimento = st.selectbox('Selecione o alimento', tabela.loc[tabela['tipo do alimento'] == tipo, 'descricao do alimento'].unique())

    with col2:  
        st.subheader('Tabela de Informações')
        
        item = tabela[(tabela['tipo do alimento'] == tipo) & (tabela['descricao do alimento'] == alimento)]
        item = item.drop(columns=['tipo do alimento', 'descricao do alimento', 'id alimento', 'umidade (%)', ])
        item = item.round(2)
        item = item.transpose()
        item.columns = ['Valor']
        st.write(item)

    st.divider()

    peso = '<p style="font-size:small;">* dados referentes a 100g do alimento.</p>'
    st.markdown(peso, unsafe_allow_html=True)

    fonte = '<p style="font-size:small;">**Fonte: Tabela Taco Unicamp.</p>'
    st.markdown(fonte, unsafe_allow_html=True)

    
    


    


if __name__ == '__main__':
    main()