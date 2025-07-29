# Importamos o Streamlit e agora a biblioteca do Google para IA Generativa
import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA IA ---
# Cole aqui a sua Chave de API que você acabou de gerar no Google AI Studio.
# É crucial que ela esteja entre as aspas.
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configura a biblioteca do Google com a sua chave.
genai.configure(api_key=GOOGLE_API_KEY)
# Define qual modelo de IA vamos usar.
modelo = genai.GenerativeModel('gemini-1.5-flash')


# --- A FUNÇÃO QUE "LIGA" PARA A IA ---
def consultar_ia(conceito):
    # Este é o "prompt", a instrução que damos para a IA.
    # É aqui que a mágica acontece. Nós dizemos como ela deve se comportar.
    prompt_template = f"""
    Aja como um professor de psicologia especialista, chamado 'Psique Explorer'.
    Sua missão é explicar o conceito psicológico '{conceito}' de forma clara, didática e estruturada para um estudante de graduação.
    Siga EXATAMENTE esta estrutura de resposta, usando os títulos marcados com ###:

    ### 👨‍🏫 Definição Formal
    [Forneça a definição técnica e acadêmica do conceito aqui.]

    ### 🗣️ 'Traduzindo' para o Português Claro
    [Dê uma analogia ou uma metáfora simples e fácil de entender sobre o conceito aqui.]

    ### 🚶‍♂️ Exemplo Prático
    [Crie um cenário ou exemplo prático e cotidiano que ilustre o conceito em ação aqui.]

    ### 🧠 Principal Teórico Associado
    [Cite o principal psicólogo ou teórico associado a este conceito.]
    """

    # Envia o prompt para o modelo Gemini e espera a resposta.
    resposta = modelo.generate_content(prompt_template)
    return resposta.text


# --- A INTERFACE DO SOFTWARE (A mesma de antes) ---
st.title("🧠 Psique Explorer v2.0 (Conectado à IA)")
st.write("Seu laboratório cognitivo de bolso, agora com o poder do Google AI.")
st.markdown("---")

conceito_usuario = st.text_input("Digite QUALQUER conceito de Psicologia para explorar:")

if st.button("Explorar Conceito"):
    if conceito_usuario:
        # Mostra uma mensagem de carregamento enquanto a "ligação" é feita.
        with st.spinner(f"Consultando a biblioteca universal sobre '{conceito_usuario}'..."):
            try:
                # Chama a função que consulta a IA em tempo real.
                resposta_formatada = consultar_ia(conceito_usuario)
                # Exibe a resposta formatada na tela.
                st.markdown(resposta_formatada)
            except Exception as e:
                # Se der algum erro (chave errada, problema de conexão), avisa o usuário.
                st.error(f"Ocorreu um erro ao conectar com a IA. Verifique sua chave de API e conexão com a internet. Detalhes: {e}")
    else:
        st.error("Por favor, digite um conceito na caixa de texto.")