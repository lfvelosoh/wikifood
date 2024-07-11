import streamlit as st
import sqlite3
import pandas as pd

 
def main():

    st.set_page_config(
        page_title="WikiFood",
        page_icon="🍔",
    )

    st.title('🔄 Comparativo')
    st.write('Compare a composição nutricional de dois alimentos.')
    st.divider()

    conn = sqlite3.connect('dados.db')
    tabela = pd.read_sql_query("SELECT * from tabela", conn)
    tabela2 = pd.read_sql_query("SELECT * from tabela", conn)
    conn.close()

    col1, col2 = st.columns(2)

    with col1:
        tipo = st.selectbox('Selecione o tipo do alimento', tabela['tipo do alimento'].unique())
        alimento = st.selectbox('Selecione o alimento', tabela.loc[tabela['tipo do alimento'] == tipo, 'descricao do alimento'].unique())

        item = tabela[(tabela['tipo do alimento'] == tipo) & (tabela['descricao do alimento'] == alimento)]
        item = item.drop(columns=['tipo do alimento', 'descricao do alimento', 'id alimento', 'umidade (%)', ])
        item = item.round(2)
        item = item.transpose()
        item.columns = ['Valor']
        st.write(item)


    with col2:
        tipo2 = st.selectbox('Selecione o tipo do alimento 2', tabela2['tipo do alimento'].unique())
        alimento2 = st.selectbox('Selecione o alimento 2', tabela2.loc[tabela2['tipo do alimento'] == tipo2, 'descricao do alimento'].unique())

        item2 = tabela2[(tabela2['tipo do alimento'] == tipo2) & (tabela2['descricao do alimento'] == alimento2)]
        item2 = item2.drop(columns=['tipo do alimento', 'descricao do alimento', 'id alimento', 'umidade (%)', ])
        item2 = item2.round(2)
        item2 = item2.transpose()
        item2.columns = ['Valor']
        st.write(item2)

    st.divider()

    small_text = '<p style="font-size:small;">* dados referentes a 100g do alimento.</p>'
    st.markdown(small_text, unsafe_allow_html=True)

    fonte = '<p style="font-size:small;">**Fonte: Tabela Taco Unicamp.</p>'
    st.markdown(fonte, unsafe_allow_html=True)

    
    


    


if __name__ == '__main__':
    main()