# Import the necessary libraries
import streamlit as st  # For creating the web app interface
from google import genai  # For interacting with the Google Gemini API

# --- 1. Page Configuration and Title ---

# Set the title and a caption for the web page
st.title("💬 Gemini Chatbot")
st.caption("A simple and friendly chat using Google's Gemini Flash model")

# --- 2. api key for Settings ---

    google_api_key = st.text('AIzaSyCiq9-aqBCaLkK5bwj6YZtQqHxhPCGz1Bc')

# --- 3. API Key and Client Initialization ---

if ("genai_client" not in st.session_state) or (getattr(st.session_state, "_last_key", None) != google_api_key):
    try:
        # If the conditions are met, create a new client.
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        # Store the new key in session state to compare against later.
        st.session_state._last_key = google_api_key
        # Since the key changed, we must clear the old chat and message history.
        # .pop() safely removes an item from session_state.
        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)
    except Exception as e:
        # If the key is invalid, show an error and stop.
        st.error(f"Invalid API Key: {e}")
        st.stop()


# --- 4. Chat History Management ---

# Initialize the chat session if it doesn't already exist in memory.
if "chat" not in st.session_state:
    # Create a new chat instance using the 'gemini-2.5-flash' model.
    st.session_state.chat = st.session_state.genai_client.chats.create(model="gemini-2.5-flash")

# Initialize the message history (as a list) if it doesn't exist.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Handle the reset button click.
if reset_button:
    # If the reset button is clicked, clear the chat object and message history from memory.
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    # st.rerun() tells Streamlit to refresh the page from the top.
    st.rerun()

# --- 5. Display Past Messages ---

# Loop through every message currently stored in the session state.
for msg in st.session_state.messages:
    # For each message, create a chat message bubble with the appropriate role ("user" or "assistant").
    with st.chat_message(msg["role"]):
        # Display the content of the message using Markdown for nice formatting.
        st.markdown(msg["content"])

# --- 6. Handle User Input and API Communication ---

# Create a chat input box at the bottom of the page.
# The user's typed message will be stored in the 'prompt' variable.
prompt = st.chat_input("Type your message here...")

# Check if the user has entered a message.
if prompt:
    # 1. Add the user's message to our message history list.
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 2. Display the user's message on the screen immediately for a responsive feel.
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Get the assistant's response.
    # Use a 'try...except' block to gracefully handle potential errors (e.g., network issues, API errors).
    try:
        # Send the user's prompt to the Gemini API.
        response = st.session_state.chat.send_message(prompt)
        
        # Safely get the text from the response object.
        # `hasattr(object, 'attribute_name')` checks if an object has a specific property.
        # This prevents an error if the API response object doesn't have a '.text' attribute.
        if hasattr(response, "text"):
            answer = response.text
        else:
            # If there's no '.text', convert the whole response to a string as a fallback.
            answer = str(response)

    except Exception as e:
        # If any error occurs, create an error message to display to the user.
        answer = f"An error occurred: {e}"

    # 4. Display the assistant's response.
    with st.chat_message("assistant"):
        st.markdown(answer)
    # 5. Add the assistant's response to the message history list.
    st.session_state.messages.append({"role": "assistant", "content": answer})
