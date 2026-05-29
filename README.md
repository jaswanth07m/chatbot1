# 🚀 AI Document Assistant

An AI-powered chatbot built using Streamlit and Groq's Llama 3.3 model. The application allows users to chat with an AI assistant, upload PDF documents, and ask questions based on the uploaded content using a lightweight Retrieval-Augmented Generation (RAG) workflow.

## 📌 Features

* 🤖 AI Chatbot powered by Llama 3.3 via Groq API
* 📄 PDF Upload and Processing
* 🔍 Retrieval-Augmented Generation (RAG)
* 💬 Chat History Support
* 🎨 Custom Streamlit UI with Dark Theme
* ⚡ Typing Animation for Responses
* 🧠 General Knowledge Fallback when information is not found in the uploaded PDF
* 📱 Responsive and User-Friendly Interface

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### AI Model

* Groq API
* Llama 3.3 70B Versatile

### PDF Processing

* PyPDF

### Text Processing

* LangChain Text Splitters

### Backend

* Python

### Environment Management

* Python Dotenv

---

## 🏗️ System Architecture

```text
User
 │
 ▼
Streamlit Chat Interface
 │
 ▼
PDF Upload (Optional)
 │
 ▼
Text Extraction using PyPDF
 │
 ▼
Chunking using LangChain
 │
 ▼
Store Chunks in Session State
 │
 ▼
Retrieve Relevant Chunks
 │
 ▼
Send Context + User Query
 │
 ▼
Groq Llama 3.3
 │
 ▼
AI Response
```

## ⚙️ How It Works

### Chatbot Workflow

1. User enters a message.
2. Message is stored in Streamlit session state.
3. Conversation history is sent to Groq's Llama 3.3 model.
4. The AI generates a response.
5. Response is displayed with a typing animation.

### PDF Question Answering Workflow

1. User uploads a PDF file.
2. Text is extracted using PyPDF.
3. The extracted text is split into smaller chunks.
4. Chunks are stored in memory.
5. When a question is asked, relevant chunks are retrieved using keyword matching.
6. Retrieved context is sent to the LLM.
7. The LLM generates an answer using the PDF content when available.

---

## 📂 Project Structure

```text
chatbot1/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
└── .venv/
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/jaswanth07m/chatbot1

cd chatbot1
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### Run Application

```bash
streamlit run app.py
```

---

## 📖 Example Use Cases

### Study Assistant

Upload course notes and ask:

```text
Explain Binary Search
```

### PDF Summarization

Upload a document and ask:

```text
Summarize this PDF
```

### Documentation Assistant

Upload technical documentation and ask questions about it.

---

## 🎯 Key Learnings

Through this project I learned:

* Building AI applications with Streamlit
* Integrating Large Language Models using APIs
* Managing application state with Streamlit Session State
* Processing PDF documents in Python
* Implementing a basic Retrieval-Augmented Generation (RAG) pipeline
* Creating interactive and responsive user interfaces
* Working with prompt engineering and context injection

---

## 🔮 Future Improvements

* Semantic Search using FAISS
* Vector Embeddings
* Multi-PDF Support
* PDF Summarization Button
* Voice Input and Output
* Chat Export Feature
* Multiple LLM Support (OpenAI, Gemini, Groq)
* User Authentication

---

## 👨‍💻 Author

Jaswanth

Built as a learning project to explore AI application development, Retrieval-Augmented Generation (RAG), and LLM integration.
"""
