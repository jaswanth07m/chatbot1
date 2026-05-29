import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#import chromadb

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Title */
h1 {
    text-align: center;
    color: white !important;
    font-size: 3rem !important;
}

/* Chat input */
.stChatInput {
    border-radius: 15px;
}

/* User messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background-color: #1e3a8a;
    border-radius: 15px;
    padding: 10px;
    margin: 10px 0;
}

/* Assistant messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background-color: #111827;
    border-radius: 15px;
    padding: 10px;
    margin: 10px 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    background-color: #2563eb;
    color: white;
    border: none;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

</style>
""", unsafe_allow_html=True)
#pdf reader
def read_pdf(file):

    pdf = PdfReader(file)

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=api_key)

# Page title
#st.set_page_config(
 #   page_title="AI Chatbot",
  #  page_icon="🤖"
#)

st.markdown("""
<h1 style='text-align:center;'>
🚀 AI Assistant
</h1>

<p style='text-align:center;color:gray;'>
Powered by Groq + Llama 3.3
</p>
""", unsafe_allow_html=True)

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        width=120
    )

    st.title("⚙ Settings")

    temperature = st.slider(
        "Creativity",
        0.0,
        1.0,
        0.8
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"]
    )

    st.write("Powered by Llama 3.3 via Groq")


#process pdf
if uploaded_file:

    text = read_pdf(uploaded_file)

    st.sidebar.write(
        f"Characters extracted: {len(text)}"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    st.session_state.pdf_chunks = chunks

    st.sidebar.success("PDF Loaded Successfully!")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type your message...")

if prompt:

    # Show user message
    with st.chat_message(
        "user",
        avatar="😎"
    ):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    try:
        #modify llm

        context = ""

        if uploaded_file and "pdf_chunks" in st.session_state:

            chunks = st.session_state.pdf_chunks

            relevant_chunks = []

            prompt_words = prompt.lower().split()

            for chunk in chunks:

                chunk_lower = chunk.lower()

                score = sum(
                    1 for word in prompt_words
                    if word in chunk_lower
                )

                if score > 0:
                    relevant_chunks.append(
                        (score, chunk)
                    )

            relevant_chunks.sort(
                reverse=True,
                key=lambda x: x[0]
            )

            top_chunks = [
                chunk
                for score, chunk
                in relevant_chunks[:3]
            ]

            context = "\n".join(top_chunks)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""
                You are a helpful AI assistant.

                Use the PDF context when it contains relevant information.

                If the PDF does not contain the answer,
                answer using your general knowledge.

                PDF Context:
                {context}
                """
                }
            ] + st.session_state.messages,
            temperature=temperature,
            max_tokens=1024
        )

        answer = response.choices[0].message.content

        import time

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            placeholder = st.empty()

            full_text = ""

            for word in answer.split():

                full_text += word + " "

                placeholder.markdown(full_text + "▌")

                time.sleep(0.03)

            placeholder.markdown(full_text)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error(f"Error: {e}")