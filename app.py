import streamlit as st
from openai import OpenAI
import time
from PIL import Image
import os
import requests
from io import BytesIO
import requests
import base64
import io

# Configuração da página
st.set_page_config(
    page_title="LEONARDO ZANETTE CLONE AI", page_icon="🤖", layout="centered"
)

# Adicione isso após a definição de st.set_page_config
st.sidebar.title("Configurações")
auto_voice_response = st.sidebar.checkbox("Respostas de voz automáticas", value=False)

# Título e descrição
st.title("ZANETTE CLONE AI")
st.markdown("Converse com o assistente de IA e receba respostas instantâneas.")


def generate_speech(text, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": st.secrets["ELEVENLABS_API_KEY"],
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.38,
            "similarity_boost": 0.75,
            "use_speaker_boost": True,
        },
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Erro ao gerar áudio: {response.status_code}")
        return None


def play_audio(audio_content):
    audio_base64 = base64.b64encode(audio_content).decode("utf-8")
    audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    st.markdown(audio_tag, unsafe_allow_html=True)


def load_avatar(image_source):
    """
    Carrega uma imagem de avatar a partir de um caminho local ou URL.

    :param image_source: String contendo o caminho local ou URL da imagem
    :return: Objeto PIL.Image ou None se a imagem não puder ser carregada
    """
    try:
        if image_source.startswith(("http://", "https://")):
            # Se for uma URL
            response = requests.get(image_source)
            img = Image.open(BytesIO(response.content))
        else:
            # Se for um caminho local
            if os.path.exists(image_source):
                img = Image.open(image_source)
            else:
                raise FileNotFoundError(f"Arquivo não encontrado: {image_source}")

        # Redimensiona a imagem para um tamanho padrão (opcional)
        img = img.resize((128, 128))
        return img
    except Exception as e:
        st.warning(f"Não foi possível carregar a imagem do avatar: {e}")
        return None


# Carregue a imagem do avatar
# Você pode usar um caminho local ou uma URL aqui
avatar_image = load_avatar(st.secrets["IMAGE_ASSISTANT_URL"])
# ou
# avatar_image = load_avatar("https://exemplo.com/caminho/para/imagem_avatar.png")


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
    for index, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant", avatar=avatar_image):
                st.markdown(message["content"])
                if st.button(
                    "Ouvir resposta", key=f"audio_{index}_{hash(message['content'])}"
                ):
                    audio_content = generate_speech(
                        message["content"], st.secrets["VOICE_ID"]
                    )
                    if audio_content:
                        play_audio(audio_content)


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

        # Substituir a parte do código que processa a resposta do assistente
        if run.status == "failed":
            st.error("Ocorreu um erro ao processar a resposta.")
        else:
            # Dentro do bloco else após verificar se run.status não é "failed"
            # Obter as mensagens do thread
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )

            # Processar apenas a resposta mais recente do assistente
            latest_response = ""
            for message in messages.data:
                if message.role == "assistant":
                    for content in message.content:
                        if content.type == "text":
                            latest_response = content.text.value
                    break  # Sair do loop após encontrar a primeira resposta do assistente

            # Adicionar apenas a resposta mais recente do assistente à sessão
            if latest_response:
                st.session_state.messages.append(
                    {"role": "assistant", "content": latest_response}
                )

                # Gerar e reproduzir áudio automaticamente se a opção estiver ativada
                if auto_voice_response:
                    audio_content = generate_speech(latest_response, st.secrets["VOICE_ID"])
                    if audio_content:
                        play_audio(audio_content)

        # Reexibir todas as mensagens
        st.rerun()


# Não é necessário chamar display_messages() aqui novamente
