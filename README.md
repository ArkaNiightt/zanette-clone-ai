# 🌟 Leonardo Zanette Clone AI - README

Este projeto implementa um clone do assistente de IA "Zanette Clone AI" usando a biblioteca Streamlit e a API da OpenAI. Ele permite que os usuários conversem com o assistente de IA e recebam respostas instantâneas de forma simples e intuitiva.

## 📋 Requisitos

- Python 3.8 ou superior
- Bibliotecas Python:
  - `streamlit`
  - `openai`

## 🚀 Instalação

1. **Clone este repositório** em seu computador:
   ```sh
   git clone https://github.com/ArkaNiightt/zanette-clone-ai.git
   cd zanette-clone-ai
   ```

2. **Crie um ambiente virtual** (opcional, mas recomendado):
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências** necessárias:
   ```sh
   pip install -r requirements.txt
   ```

4. **Crie um arquivo `secrets.toml`** para armazenar suas chaves de API:
   ```toml
   [secrets]
   OPENAI_API_KEY = "sua-chave-api-openai"
   OPENAI_ASSISTANT_ID = "seu-assistente-id"
   ```

## ▶️ Como Executar

Execute o comando abaixo para iniciar o servidor Streamlit:

```sh
streamlit run app.py
```

Depois de iniciar o servidor, abra o link local fornecido (normalmente `http://localhost:8501`) no navegador para acessar a interface do assistente de IA.

## ✨ Funcionalidades

- **💬 Conversação Instantânea:** Interaja com o assistente de IA enviando mensagens e receba respostas instantâneas em uma interface amigável.
- **📜 Histórico de Conversas:** As mensagens enviadas e recebidas são armazenadas na sessão do Streamlit, permitindo acompanhar toda a conversa.
- **🧹 Limpar Histórico:** Use o botão na barra lateral para limpar o histórico de conversas e começar um novo diálogo a qualquer momento.

## 🛠️ Organização do Código

- **Configuração da Página:** Define o título, o ícone e a largura da página para melhorar a experiência do usuário.
- **Inicialização do Cliente OpenAI:** Configura a autenticação com a API da OpenAI utilizando as chaves de API fornecidas.
- **Gerenciamento de Sessão:** Utiliza a sessão do Streamlit para armazenar as mensagens e o `thread_id` do assistente, garantindo continuidade nas conversas.
- **Funções Auxiliares:**
  - `display_messages()`: Exibe as mensagens salvas na sessão, mantendo o histórico da conversa visível.
  - `clear_history()`: Limpa o histórico de conversas e exclui o `thread` associado na API da OpenAI.

## 📌 Utilização

1. **Enviar Mensagens:** Use a caixa de entrada na parte inferior da página para enviar mensagens para o assistente de IA e receber respostas instantâneas.
2. **Limpar Histórico:** Caso queira começar uma nova conversa, clique no botão "Limpar Histórico" localizado na barra lateral para apagar todo o histórico atual.
3. **Interação com o Assistente:** Sempre que uma mensagem é enviada, o assistente é acionado e a resposta correspondente é exibida na tela, criando uma experiência de diálogo contínua.

## 💡 Dicas de Uso

- **⏱️ Respostas Rápidas:** O assistente pode demorar alguns segundos para gerar uma resposta dependendo da complexidade do prompt. Aguarde enquanto o indicador de "Aguardando resposta..." estiver ativo.
- **🔑 API da OpenAI:** Garanta que suas chaves de API estejam corretas e ativas para evitar erros de autenticação.
- **📂 Ambiente Virtual:** Utilizar um ambiente virtual é uma boa prática para evitar conflitos de dependências com outras aplicações Python instaladas no seu sistema.

## ⚠️ Considerações

- Este código faz uso de recursos da API OpenAI que podem estar em versões beta e estão sujeitos a mudanças. Certifique-se de verificar a documentação oficial para atualizações.
- Para que a integração funcione, é necessário ter uma chave de API válida da OpenAI e um ID de assistente que tenha sido criado previamente na plataforma OpenAI.

## 📜 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para contribuir, adaptar e utilizar conforme necessário. Se encontrar algum problema ou tiver sugestões, contribuições são sempre bem-vindas!

## 🤝 Contribuindo

Contribuições são incentivadas! Siga as etapas abaixo para contribuir com melhorias:

1. **Faça um fork** do repositório.
2. **Crie uma branch** para sua feature (`git checkout -b feature/nova-feature`).
3. **Commit suas alterações** (`git commit -m 'Adiciona nova feature'`).
4. **Envie para o repositório remoto** (`git push origin feature/nova-feature`).
5. **Abra um Pull Request**.

## 📧 Contato

Para quaisquer dúvidas ou feedback, sinta-se à vontade para entrar em contato pelo GitHub ou através do e-mail `narutogoit@gmail.com`.

