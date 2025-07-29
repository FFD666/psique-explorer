# Importamos as bibliotecas necessárias
import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA IA ---
# Esta parte é crucial. O Streamlit vai ler a chave do "cofre" (Secrets)
# que configuramos na plataforma Streamlit Community Cloud.
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    modelo = genai.GenerativeModel('gemini-1.5-flash')
except (FileNotFoundError, KeyError):
    # Este bloco é um fallback para quando rodamos o app localmente
    # e não temos um arquivo de secrets. Ele procura a chave em outro lugar.
    # Se você for testar localmente, precisará configurar isso.
    # Por enquanto, focaremos no funcionamento online.
    st.error("Chave de API do Google não encontrada. Configure-a nos 'Secrets' do Streamlit Cloud.")
    st.stop()


# --- INTERFACE DO APLICATIVO ---
st.title("🧠 Psique Explorer v3.0")
st.caption("Seu tutor de psicologia com IA, agora com conversas abertas.")

# Permite ao usuário escolher sua "persona"
persona_selecionada = st.radio(
    "Como você gostaria de interagir com a IA?",
    ('Estou aqui para Aprender (Estudante)', 'Estou aqui para Debater (Professor)'),
    horizontal=True
)

# Define o comportamento inicial da IA com base na persona
if persona_selecionada == 'Estou aqui para Aprender (Estudante)':
    prompt_inicial = {
        "role": "model",
        "parts": ["Aja como um tutor de psicologia chamado 'Psique Explorer'. Você é paciente, didático e adora usar analogias e exemplos práticos. Seu objetivo é ajudar estudantes de graduação a entenderem conceitos complexos de forma simples. Comece se apresentando e perguntando qual o tópico de hoje."]
    }
else: # Professor
    prompt_inicial = {
        "role": "model",
        "parts": ["Aja como um colega acadêmico especialista em psicologia. Você é preciso, técnico e capaz de debater nuances teóricas, comparar autores e sugerir materiais de pesquisa. Assuma que o usuário tem conhecimento prévio. Comece se apresentando de forma profissional e se colocando à disposição para o debate."]
    }

# --- GERENCIAMENTO DA MEMÓRIA DA CONVERSA ---
# Usamos o 'st.session_state' para que o app não esqueça o histórico do chat
if "historico_chat" not in st.session_state or st.session_state.get('persona_anterior') != persona_selecionada:
    st.session_state.historico_chat = [prompt_inicial]
    st.session_state.persona_anterior = persona_selecionada

# Inicia o modelo de chat com o histórico guardado
chat = modelo.start_chat(history=[m for m in st.session_state.historico_chat if m['role'] != 'model' or len(st.session_state.historico_chat) == 1])


# --- EXIBIÇÃO DO CHAT ---
# Mostra as mensagens antigas na tela
for mensagem in st.session_state.historico_chat:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["parts"][0])

# Pede por uma nova mensagem do usuário
if prompt_usuario := st.chat_input("Digite sua mensagem..."):
    # Adiciona a mensagem do usuário ao histórico e exibe na tela
    st.session_state.historico_chat.append({"role": "user", "parts": [prompt_usuario]})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    # Envia a conversa para a IA e espera a resposta
    with st.chat_message("model"):
        message_placeholder = st.empty()
        resposta_completa = ""
        try:
            # Envia a nova mensagem para o chat continuar a conversa
            resposta = chat.send_message(prompt_usuario, stream=True)
            for chunk in resposta:
                resposta_completa += chunk.text
                message_placeholder.markdown(resposta_completa + "▌")
            message_placeholder.markdown(resposta_completa)
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar sua mensagem. Verifique sua chave de API ou conexão. Detalhes: {e}")