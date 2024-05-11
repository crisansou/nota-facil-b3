import streamlit as st
from src.views.nota_corretagem_view import NotaCorretagemView

# Inicializa a página com título e ícone.
st.set_page_config(page_title="Ler Notas", page_icon="📄")

# Cria uma instância da view e renderiza a página.
NotaCorretagemView().render()