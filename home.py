import streamlit as st
import sqlite3
import pandas as pd

 
def main():

    st.set_page_config(
        page_title="WikiFood",
        page_icon="🍔",
    )

    st.title('🥗 Home')

    text = 'Bem vindo ao <b>🍔 WikiFood </b>, um site para consulta de informações nutricionais de alimentos.'
    st.markdown(text, unsafe_allow_html=True)

   
    st.write('Escolha uma das opções no menu lateral para começar.')


if __name__ == '__main__':
    main()