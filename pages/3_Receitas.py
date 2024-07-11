import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def main():

    st.set_page_config(
        page_title="WikiFood",
        page_icon="🍔",
    )

    st.title('🫕 Receitas')
    st.write('Adicione os alimentos que você deseja incluir na sua receita e veja a composição nutricional da mesma.')
    st.divider()

    if 'pd_alimentos' not in st.session_state:
        st.session_state.pd_alimentos = pd.DataFrame(columns=['alimento', 'quantidade', 'lipideos (g)', 'carboidrato (g)', 'proteina (g)', 'energia (kcal)'])

    conn = sqlite3.connect('dados.db')
    tabela = pd.read_sql_query("SELECT * from tabela", conn)
    conn.close()

    tipo = st.selectbox('Selecione o tipo do alimento', tabela['tipo do alimento'].unique())
    alimento = st.selectbox('Selecione o alimento', tabela.loc[tabela['tipo do alimento'] == tipo, 'descricao do alimento'].unique())
    quantidade = st.number_input('Quantidade (g)', value=0)
    
    if st.button('Inserir'):
        novo_registro = pd.DataFrame({'alimento': [alimento], 'quantidade': [quantidade]})
        novo_registro['lipideos (g)'] = tabela.loc[tabela['descricao do alimento'] == alimento, 'lipideos (g)'].values[0] * quantidade / 100
        novo_registro['carboidrato (g)'] = tabela.loc[tabela['descricao do alimento'] == alimento, 'carboidrato (g)'].values[0] * quantidade / 100
        novo_registro['proteina (g)'] = tabela.loc[tabela['descricao do alimento'] == alimento, 'proteina (g)'].values[0] * quantidade / 100
        novo_registro['energia (kcal)'] = tabela.loc[tabela['descricao do alimento'] == alimento, 'energia (kcal)'].values[0] * quantidade / 100
        st.session_state.pd_alimentos = pd.concat([st.session_state.pd_alimentos, novo_registro], ignore_index=True)
    
    if st.button('Limpar'):
        st.session_state.pd_alimentos = pd.DataFrame(columns=['alimento', 'quantidade'])

    if st.session_state.pd_alimentos.empty:
        st.write('Nenhum alimento cadastrado')
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader('Alimentos')
            
            st.write(st.session_state.pd_alimentos)
        with c2:
            st.subheader("Macro Nutrientes")

            # Calculate the sum of lipideos, carboidrato, and proteina
            lipideos_sum = round(st.session_state.pd_alimentos['lipideos (g)'].sum(), 2)
            carboidrato_sum = round(st.session_state.pd_alimentos['carboidrato (g)'].sum(), 2)
            proteina_sum = round(st.session_state.pd_alimentos['proteina (g)'].sum(), 2)

            # Create a pie chart
            labels = ['Lipideos', 'Carboidrato', 'Proteina']
            sizes = [lipideos_sum, carboidrato_sum, proteina_sum]
            colors = ['blue', 'green', 'orange']
            explode = (0, 0, 0)  # explode the first slice


            plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.gca().patch.set_alpha(0)  # Set the background of the plot to be transparent

            # Display the pie chart
            st.pyplot(plt)

            st.write('Lipideos (g):', lipideos_sum)
            st.write('Carboidrato (g):', carboidrato_sum)
            st.write('Proteina (g):', proteina_sum)
            st.write('Energia (kcal):', round(st.session_state.pd_alimentos['energia (kcal)'].sum(),2))


            
    
    


if __name__ == '__main__':
    main()