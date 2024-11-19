# AssistAI

AssistAI is a personal assistant based on artificial intelligence that uses **Streamlit** to provide an interactive interface. The application connects to a completions API compatible with OpenAI, allowing users to interact in a simple and efficient manner.

## Main Features
- **Real-Time Interaction**: Users can enter prompts and receive instant responses.
- **AI-Based**: Utilizes a language model hosted via Ollama to provide intelligent answers.
- **Intuitive Interface**: The application is built with Streamlit, providing a user-friendly experience.


## Installation
Follow the steps below to install and run AssistAI:

### Prerequisites

[Docker e Docker Compose](https://www.docker.com/get-started/) installed on your machine. 

### Installation Steps


1. **Clone the Repository:**


```bash
git clone https://github.com/lucasarnalves/AssistAI.git
cd AssistAI
```

2. **Directory Structure:**

Ensure that the directory structure is correct:

```
AssistAI/
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

3. Modify the **'.env.example'** file to select the Ollama model to be used and rename it to .env

```bash
mv .env.exemple .env
```

4. **Adjust Script Permissions:**

After cloning the repository, ensure that the *'start_ollama.sh'* script has execution permissions:

```bash
chmod +x start_ollama.sh
```

5. **Build and Start the Application:** 

Run the following command to build the images and start the containers:


```bash
docker compose up --build
```

6. **Access the Application:** Open your browser and go to *http://localhost:8501* to interact with AssistAI.


## Contributions

Feel free to contribute improvements and new features. Open a pull request or create an issue to discuss your ideas!
