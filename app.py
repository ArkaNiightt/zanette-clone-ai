import streamlit as st
from openai import OpenAI
import time

# Configuração da página
st.set_page_config(
    page_title="LEONARDO ZANETTE CLONE AI", page_icon="🤖", layout="wide"
)

# Título e descrição
st.title("ZANETTE CLONE AI")
st.markdown("Converse com o assistente de IA e receba respostas instantâneas.")


# Inicializando o cliente OpenAI
@st.cache_resource
def get_openai_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


client = get_openai_client()


# Recuperar um assistente já criado na plataforma OpenAI
@st.cache_resource
def get_assistant():
    return client.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT_ID"])


my_assistant = get_assistant()

# Inicializando mensagens e thread na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None


# Função para exibir mensagens
def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Função para limpar o histórico
def clear_history():
    st.session_state.messages = []
    if st.session_state.thread_id:
        try:
            client.beta.threads.delete(st.session_state.thread_id)
        except Exception as e:
            st.error(f"Erro ao deletar o thread: {e}")
    st.session_state.thread_id = None


# Botão para limpar o histórico
if st.sidebar.button("Limpar Histórico"):
    clear_history()
    st.rerun()

# Exibindo as mensagens anteriores
display_messages()

# Caixa de entrada para o usuário enviar uma nova mensagem
if prompt := st.chat_input("Mande uma mensagem"):
    # Adicionar a mensagem do usuário à sessão
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Criar um novo thread se não existir
    if not st.session_state.thread_id:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # Adicionar a mensagem do usuário ao thread
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id, role="user", content=prompt
    )

    # Executar o assistente
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id, assistant_id=my_assistant.id
    )

    # Aguardar a conclusão da execução
    with st.spinner("Aguardando resposta..."):
        while run.status not in ["completed", "failed"]:
            time.sleep(0.5)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id, run_id=run.id
            )

    if run.status == "failed":
        st.error("Ocorreu um erro ao processar a resposta.")
    else:
        # Obter as mensagens do thread
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Processar a resposta do assistente
        full_response = ""
        for message in messages:
            if message.role == "assistant":
                for content in message.content:
                    if content.type == "text":
                        full_response += content.text.value

        # Adicionar a resposta do assistente à sessão
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

    # Reexibir todas as mensagens
    st.rerun()

# Não é necessário chamar display_messages() aqui novamente
