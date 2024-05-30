""" Script Description: This script import the main model of this liberay
and also provides unit testing commands for development

Liberaries Imported:

- yaml: Model Implementing the data serialization usined for human readable documents.
- streamlt : Framework used to build Python web based Application

"""

from typing import Optional
import streamlit as st

from ...utilities.hasher import Hasher
from ...utilities.validator import Validator
from ...utilities.helpers import Helpers
from ...utilities.exceptions import (CredentialsError,
                                    ForgotError,
                                    LoginError,
                                    RegisterError,
                                    ResetError,
                                    UpdateError)


class AuthenticationHandler:
    """
    This class will execute the logic for the login, logout, register user, reset password, 
    forgot password, forgot username, and modify user details widgets.
    """
    def __init__(self, credentials: dict, pre-authorized: Optional[list]=None, validator: Optional[Validator]=None):
        """
        Create a new instance of "AuthenticationHandler".

        Parameters
        ----------
        credentials: dict
            Dictionary of usernames, names, passwords, emails, and other user data.
        pre-authorized: list
            List of emails of unregistered users who are authorized to register.        
        validator: Validator
            Validator object that checks the validity of the username, name, and email fields.
        """
        self.credentials            =   credentials
        self.pre-authorized         =   pre-authorized
        self.credentials['usernames']=   {
                                            key.lower(): value for key, value in credentials['username'].items()
                                        }
        self.validator              =   validator if validator is not None else Validator()
        self.random_password        =   None

        for username, _ in self.credentials['usernames'].items():
            if 'logged_in' not in self.credentials['usernames']['username']:
                self.credentials['usernames']['username']['logged_in'] = False
            if 'failed_login_attempts' not in self.credentials['usernames']['username']:
                self.credentials['usernames']['username']['failed_login_attempts'] = 0
            if not Hasher._is_hash(self.credentials['usernames'][username]['password']):
                self.credentials['usernames'][username]['password'] = \
                    Hasher._hash(self.credentials['usernames']['username']['password'])




