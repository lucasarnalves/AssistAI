# AssistAI

AssistAI é um assistente pessoal baseado em inteligência artificial que utiliza *Streamlit* para fornecer uma interface interativa. A aplicação se conecta a uma API de completions compatível com OpenAI, permitindo que os usuários interajam de forma simples e eficiente.


## Funcionalidades Principais
Interação em Tempo Real: Os usuários podem inserir prompts e receber respostas instantaneamente.
Baseado em IA: Utiliza um modelo de linguagem hospedado via ollama para fornecer respostas inteligentes.
Interface Intuitiva: A aplicação é construída com Streamlit, proporcionando uma experiência de usuário amigável.


## Instalação
Siga os passos abaixo para instalar e executar o AssistAI:

### Pré-requisitos

Docker e Docker Compose instalados na sua máquina.

#### Passos de Instalação

1 - Clone o Repositório:


```bash
git clone https://github.com/seu_usuario/assistai.git
cd assistai
```

2 - Estrutura de Diretórios: Certifique-se de que a estrutura de diretórios está correta:

```
assistai/
├── app/
│   ├── main.py
│   └── requirements.txt
├── models/
├── docker-compose.yml
├── env.exemple
├── Dockerfile
├── start_ollama.sh
├── .gitignore
└── README.md
```

3 - Modifique o arquivo '.env.exemple' para selecionar o modelo ollama a ser utilizado e renomeie para .env

```bash
mv .env.exemple .env
```

4 - Construir e Subir a Aplicação: Execute o seguinte comando para construir as imagens e iniciar os contêineres:


```bash
docker-compose up --build
```

5- Acessar a Aplicação: Abra seu navegador e acesse *http://localhost:8501* para interagir com o AssistAI.


## Contribuições

Sinta-se à vontade para contribuir com melhorias e novas funcionalidades. Abra um pull request ou crie uma issue para discutir suas ideias!
