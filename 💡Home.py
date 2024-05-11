import base64
import streamlit as st

st.set_page_config(page_title="Home", page_icon="💡",)

# Insere links para o GitHub e LinkedIn
st.markdown(
    """
    <div style='text-align: center; padding-top: 30px;'>
    <a href="https://github.com/crisansou/nota-facil-b3" target="_blank">GitHub</a> | 
    <a href="https://www.linkedin.com/in/cristina-santana-souza/" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("# Bem vindo ao Nota Fácil B3! 👋")

st.subheader("Cansado de decifrar suas notas de corretagem?", divider='blue')

st.markdown(
    """
    Com tantas corretoras e diferentes formatos de nota, analisar seus investimentos pode ser uma tarefa complexa e demorada. 
    É por isso que criamos o **Nota Fácil B3**, uma ferramenta inteligente que simplifica este processo para você!  
    
    ### O que ela faz?

    Nossa ferramenta, utilizando a inteligência artificial do Google Gemini, é capaz de:
    - Ler e interpretar automaticamente notas de corretagem de diversas corretoras, independentemente do formato.
    - Extrair informações importantes, como:
        - Corretora
        - Número da nota
        - Data do pregão
        - Valor total da nota
        - Custos operacionais
        - Ativos negociados
        - Quantidade, preço e valor de cada operação
        - Preço médio de cada ativo
    - Para os ativos negociados acessamos o **Yahoo Finance** e criamos um gráfico com o preço dos ativos no **último ano**, desta forma conseguimos ter uma ideia se foi uma boa aquisição ou não 

    ### Como isso facilita a sua vida?
    - **Economia de tempo:**  Você não precisa mais perder analisando manualmente os dados da nota, o Gemini faz isso por você!
    - **Análise mais rápida e eficiente:** A análise do preço médio vai facilitar o seu controle e apuração de imposto de renda

    Clique em **Ler Notas** no menu lateral para começar!
    
"""
)