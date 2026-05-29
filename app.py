import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from utils.loader import load_pdf
from utils.embedder import create_embeddings
from utils.retriever import build_index
from utils.retriever import retrieve

from sentence_transformers import SentenceTransformer


@st.cache_resource
def get_embedding_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

embedding_model = get_embedding_model()
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
        if "chunks" in st.session_state:
            del st.session_state.chunks

        if "index" in st.session_state:
            del st.session_state.index

        st.rerun()

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"]
    )

    st.write("Powered by Llama 3.3 via Groq")


#process pdf
if (
    uploaded_file
    and "index" not in st.session_state
):

    chunks = load_pdf(
        uploaded_file
    )

    embeddings = create_embeddings(
        chunks
    )

    index = build_index(
        embeddings
    )

    st.session_state.chunks = chunks

    st.session_state.index = index

    st.sidebar.write(
        f"Chunks Created: {len(chunks)}"
    )

    st.sidebar.success(
        "PDF Loaded Successfully!"
    )



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

        top_chunks = []

        if (
        uploaded_file
        and "chunks" in st.session_state
        ):

            query_embedding = embedding_model.encode(
                prompt
            )

            top_chunks = retrieve(
                query_embedding,
                st.session_state.index,
                st.session_state.chunks,
                k=3
            )

            context = "\n".join(
                top_chunks
            )


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

            if top_chunks:

                with st.expander(
                    "📚 Retrieved Context"
                ):

                    for i, chunk in enumerate(
                        top_chunks
                    ):

                        st.markdown(
                            f"### Chunk {i+1}"
                        )

                        st.write(chunk)

    except Exception as e:
        st.error(f"Error: {e}")

