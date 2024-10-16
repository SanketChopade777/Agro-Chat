import os
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini_pro_model
import webbrowser

# Get the working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

# Setting up the page configuration
st.set_page_config(
    page_title="Agro-Pro | AgroChat | Team Indra",
    page_icon="🧠",
    layout="centered"
)

# Sidebar menu with link and chat option
with st.sidebar:
    selected = option_menu(
        "Agro-Pro",
        ["AgroChat", "🏠Home"],
        menu_icon='robot',
        icons=['chat-dots-fill'],
        default_index=0
    )

# If "Go to External Site" is selected, open a new browser tab
if selected == "🏠Home":
    url = "https://www.example.com"  # Replace with the actual URL
    webbrowser.open(url)

# Function to translate role between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == 'model' else user_role

# If "AgroChat" is selected, load the chat interface
if selected == "AgroChat":
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Streamlit page title
    st.title("🤖 AgroChat")
    st.markdown("<h5>Ask your questions related to agriculture!</h5>", unsafe_allow_html=True)

    # Display the chat history in a more structured way
    if "chat_session" in st.session_state:
        chat_history = st.session_state.chat_session.history
        for message in chat_history:
            with st.chat_message(translate_role_for_streamlit(message.role)):
                st.markdown(f"<div style='padding: 10px; border-radius: 5px; margin: 5px 0; background-color: #f1f1f1;'>{message.parts[0].text}</div>", unsafe_allow_html=True)

    # Input field for user's message
    user_prompt = st.chat_input("Ask AgroChat....")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro response with better styling
        with st.chat_message("assistant"):
            st.markdown(f"<div style='padding: 10px; border-radius: 5px; margin: 5px 0; background-color: #d4edda;'>{gemini_response.text}</div>", unsafe_allow_html=True)
