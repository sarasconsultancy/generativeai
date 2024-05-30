""" Script Description: This script import the main model of this liberay
and also provides unit testing commands for development

Liberaries Imported:

- yaml: Model Implementing the data serialization usined for human readable documents.
- streamlt : Framework used to build Python web based Application

"""

import yaml
import streamlit as st
import streamlit.components.v1 as components
from yaml.loader import SafeLoader
from .authenticate import authenticate
from .utilities.exceptions import (CredentialsError,
                                    ForgotError,
                                    LoginError,
                                    RegisterError,
                                    ResetError,
                                    UpdateError)

_RELEASE = True

if not _RELEASE:
    # Loading Config File
    with open('../config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)

    #Creating the authenticator Object
    autheticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )

    # Creating a Login Widget

    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)
    
    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'welocme *{st.session_state["name"]}*')
        st.title('Some Content')
    elif st.session_state["authentication_status"] is false:
        st.error('Username/Password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Creating a Password reset widget
    if st.session_state["authentication_status"]:
        try:
            if autheticator.reset_password(st.session_state["username"]):
                st.success('Password Modified Successfully')
            except ResetError as e:
                st.error(e)
            except CredentialsError as e:
                st.error(e)

    # Creating a forgot password widget
    try:
        (username_of_forgotten_password, email_of_forgotton_password, new_random_password) = authenticator.forgot_password()
        if username_of_forgotten_password:
            st.success('New Password Sent Securely')
        elif not username_of_forgotten_password:
            st.error('Username Not Found')
    except ForgotError as e:
        st.error(e)

    #Creating a Forgot username widget
    try:
        (username_of_forgotten_username, email_of_forgotton_username) = authenticator.forgotton_username()
        if username_of_forgotten_username:
            st.success('Username Send Securely')
        elif not username_of_forgotten_username:
            st.error('Email not found')
    except ForgotError as e:
        st.error(e)

    # Creating an Update user details widget
    if st.session_state["authentication_status"]:
        try:
            if authenticator.update_user_details(st.session_state["username"]):
                st.success('Entries Updated Successfully')
            except UpdateError as e:
                st.error(e)

    #Saving config file
    with open('../config.yaml','w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)











    

