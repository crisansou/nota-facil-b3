import base64
import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import yfinance as yf

from src.analysis import analyze_brokerage_note
from src.utils import extract_text_from_pdf

class NotaCorretagemView:
    """
    View para processar e exibir informações de notas de corretagem.
    """

    def __init__(self):
        """
        Inicializa a view com a API Key do Google Gemini e o logo da B3.
        """
        self.api_key = "INFORME SUA API KEY AQUI"
        self.b3_logo = self._load_image("./images/b3.png")

    def render(self):
        """
        Renderiza a página da view.
        """
        st.markdown(f"<p style='text-align: right;'>{self._image_to_html(self.b3_logo)}</p>", unsafe_allow_html=True)
        st.header("Carregue a nota de corretagem em PDF")

        uploaded_file = st.file_uploader("Escolha aqui:", type="pdf")
        if uploaded_file is not None:
            self._process_uploaded_file(uploaded_file)

    def _process_uploaded_file(self, uploaded_file):
        """
        Processa o arquivo PDF carregado, extraindo texto, analisando dados e exibindo resultados.
        """
        with st.spinner("Processando, aguarde..."):
            pdf_data = uploaded_file.read()
            pdf_text = extract_text_from_pdf(pdf_data)
            analysis_result, json_result = analyze_brokerage_note(pdf_text, self.api_key)

            st.write(analysis_result)

            st.header("Geração de gráfico com os ativos da nota")
            df = pd.DataFrame(json_result)
            st.write(df)
            self._display_stock_performance(df)

    def _display_stock_performance(self, df):
        """
        Exibe o desempenho dos ativos em um gráfico.
        """
        df["Ticker_SA"] = df["Ticker"] + ".SA"
        data_inicio = dt.date.today() - dt.timedelta(days=365)
        data_fim = dt.date.today().strftime("%Y-%m-%d")

        precos = self._fetch_stock_prices(df, data_inicio, data_fim)
        precos.columns = precos.columns.str.replace(".SA", "")

        fig, ax = plt.subplots(figsize=[12, 7])

        for col in precos.columns:
            plt.plot(precos[col], label=col)

        plt.xticks(rotation=45)
        ax.set_title('Comparação dos ativos no período de um ano', fontsize=18)
        ax.set_xlabel('Período')
        ax.set_ylabel('Preços')
        plt.legend()
        st.pyplot(fig)

    def _fetch_stock_prices(self, df, data_inicio, data_fim):
        """
        Busca os preços dos ativos no Yahoo Finance.
        """
        precos = pd.DataFrame()
        for i in df.Ticker_SA:
            ticker = yf.Ticker(i)
            precos[i] = ticker.history(start=data_inicio, end=data_fim)["Close"]
        return precos

    def _load_image(self, img_path):
        """
        Carrega uma imagem e a codifica em base64.
        """
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    def _image_to_html(self, img_data):
        """
        Converte dados de imagem codificados em base64 para HTML.
        """
        return f"<img src='data:image/png;base64,{img_data}' class='img-fluid'>"