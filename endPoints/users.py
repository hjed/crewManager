"""
The file stores functions for user related endpoints in the Crew Manger API
Created: 2/06/2015
Aurthor: Harry J.E Day
"""

import logic.Users as Users
import logic.errorCodes as errorCodes

from protorpc import messages
from protorpc import message_types
from protorpc import remote

#Represents a request to login
class LoginRequest(messages.Message):
    #the email of the user trying to login
    email = messages.StringField(1,required=True)
    #the password of the user trying to login
    #this is sent under ssl, but in plaintext
    password = messages.StringField(2,required=True)

class LoginResponse(messages.Message):
    #the session key / token the user can use to authenticate their requests
    tokenKey = messages.StringField(1, required=False)
    #the status of the request
    status = messages.IntegerField(2, required=True)
    #the error message of the request (if the request fails)
    errorMessage = messages.StringField(3, required=False)
    
class api():
    
    @staticmethod
    def doLogin(req):
        resp = LoginResponse(status = 1)
        
        (resp.status, user, token) = Users.User.login(req.email, req.password)
        if resp.status == 0:
            resp.tokenKey = token.key.urlsafe()
        else:
            resp.errorMessage = errorCodes.ERROR_CODES[resp.status]
        
        return resp