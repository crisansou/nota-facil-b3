import google.generativeai as genai
import json

def analyze_brokerage_note(pdf_text, api_key):
    """Analisa uma nota de corretagem usando o Google Gemini.

    Args:
        pdf_text (str): Texto extraído da nota de corretagem.
        api_key (str): Chave de API do Google Gemini.

    Returns:
        analysis_data (str): Resposta do modelo Gemini sobre a análise da nota.
        json_data (str): Um dicionário contendo os dados extraídos em formato JSON.
    """
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.5,   # Reduza a temperatura para respostas mais deterministas
        "top_p": 0.8,         # Ajuste o top_p para controlar a criatividade
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    system_instruction = "Você é um sistema que irá ler e detalhar as notas de corretagem da bolsa de valores do Brasil (B3)"

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        generation_config=generation_config,
        system_instruction=system_instruction,
        safety_settings=safety_settings,
    )

    # Solicitação detalhada para extrair informações
    extraction_instruction = """
        "Analise a nota de corretagem e gere uma resposta no formato a seguir usando a mesma fonte, sem exibir dados sensíveis como nome da pessoa + CPF e agrupar o resultado pelo campo 'Especificação do titulo' somando as quantidades e valor):\n\n"
        "## Análise da Nota de Corretagem\n\n"
        "**Corretora:** [Nome da corretora]\n\n"
        "**Número da Nota:** [Número da nota (campo 'Nr. nota' sem adicionar depois o D ou C)]\n\n"
        "**Data do Pregão:** [Data do Pregão  (campo 'Data pregão')]\n\n"
        "**Valor Total da Nota:** [Valor Total da Nota (campo 'Líquido para')]\n\n"
        "**Total dos Custos Operacionais:** [Total dos Custos Operacionais (explicar custo sem adicionar depois o D ou C)]\n\n"
        "**D/C da Nota:** [D/C da Nota (mostrar Débito ou Crédito)]\n\n"
        "| Ticker | C/V | Quantidade | Preço | ... |\n"
        "|---|---|---|---|---|\n"
        "| [Código do Ativo 1 (Ler a informação da coluna 'Especificação do titulo' e pesquisar no site da B3 qual é o código do ativo usando o nome, exemplo ABEV3, BOVESPA não deve ser usado como nome do ativo. Se não encontrar verificar se o código do ativo não está no nome do arquivo)] | [C/V (Colocar Compra ou Venda)] | [Quantidade 1] | [Preço 1] | [Valor 1] [Preço Médio do Ativo 1 (Calculado como (Valor Total do Ativo + Custos Operacionais Relacionados ao Ativo) / Quantidade do Ativo se for compra e substraindo se for venda)] | [D/C do Ativo (mostrar Débito ou Crédito)]"
        "| [Código do Ativo 2 (Ler a informação da coluna 'Especificação do titulo' e pesquisar no site da B3 qual é o código do ativo usando o nome, exemplo VALE3, BOVESPA não deve ser usado como nome do ativo. Se não encontrar verificar se o código do ativo não está no nome do arquivo)] | [C/V (Colocar Compra ou Venda)] | [Quantidade 2] | [Preço 2] | [Valor 2] [Preço Médio do Ativo 2 (Calculado como (Valor Total do Ativo + Custos Operacionais Relacionados ao Ativo) / Quantidade do Ativo se for compra e substraindo se for venda)] | [D/C do Ativo (mostrar Débito ou Crédito)]"
        "... (outras linhas da tabela) ...\n\n"
        "\n\n"
        "**Observações:**\n\n"
        "* [Observação 1]\n"
        "* [Observação 2]\n"
    """

    convo = model.start_chat(
        history=[
            {"role": "user", "parts": extraction_instruction},
            {"role": "user", "parts": [f"Analise a nota de corretagem:\n\n{pdf_text}"]},
        ]
    )

    convo.send_message(extraction_instruction)

    if convo.last is not None:
        analysis_data = convo.last.text
        try:
            # Adiciona a resposta do modelo ao histórico
            convo.history.append({
                "role": "model",
                "parts": analysis_data 
            })

            # Faz uma nova chamada solicitando o JSON
            convo.send_message("Gere um arquivo JSON com o resultado da tabela sem incluir a string literal ```json```.")

            # Converte a resposta do modelo (JSON) para um dicionário
            json_data = json.loads(convo.last.text)

            return analysis_data, json_data
        
        except json.JSONDecodeError:
            return analysis_data, "Erro: O modelo não gerou um JSON válido: " + convo.last.text
    else:
        return "Erro: O modelo não gerou uma resposta.", None

