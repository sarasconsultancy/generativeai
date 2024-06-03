import pickle
from pathlib import Path
import streamlit_authenticator as stauth
#from streamlit_authenticator.utilities.hasher import Hasher

names = ["Arun", "Tanzeem"]
usernames = ["arun", "tanzeem"]
passwords = ["arun123", "tanzeem123"]
#passwords = ["XXX", "XXX"]

hashed_passwords = stauth.Hasher(passwords).generate()  #bcrypt algorithm

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)