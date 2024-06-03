from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables
import streamlit as st
import os
import google.generativeai as genai
import streamlit_authenticator as stauth
import pickle
from pathlib import Path

st.set_page_config(page_title="Q&A Demo")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

#Authentication
# --- USER AUTHENTICATION ----

names = ["Arun","Tanzeem"]
usernames = ["arun","tanzeem"]

#Load Hashed Password
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

#Initialize the authenticator

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    'Q&A Demo',
    'abcdef',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("Username/Password is Incorrect")
elif authentication_status == None:
    st.error("Please enter your username and password")
elif authentication_status:
    st.header("Gemini LLM Application")

    #Initialize session state for chat histroy if it doesnt exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    @st.cache
    def get_gemini_response(question):
        response=chat.send_message(question,stream=True)
        return response

    ##initialize our streamlit app
    input=st.text_input("Input: ",key="input")
    submit=st.button("Ask the question")

    if submit and input:
        response=get_gemini_response(input)
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
    st.subheader("The Chat History is")
        
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"welcome {name}")
        